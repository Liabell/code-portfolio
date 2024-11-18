const express = require("express");
const mongoose = require("mongoose");
const File = require("./models/File"); // Import File model
const cors = require("cors");
const http = require("http");
const socketIo = require("socket.io");
const PeerServer = require('peer').PeerServer;
const { exec } = require("child_process");
const fs = require("fs"); // Import fs to manage files

// Initialize Express and HTTP server
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:3000", // Allow frontend to connect from this URL
    methods: ["GET", "POST", "DELETE"],
    allowedHeaders: ["Content-Type"],
    credentials: true,
  },
});

// Middleware
app.use(express.json());
app.use(cors({
  origin: "http://localhost:3000", // Allow requests from the frontend domain
  credentials: true,              // Allow cookies or credentials if needed
}));

// Connect to MongoDB
mongoose.connect("mongodb://localhost:27017/collabDB", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("MongoDB connection error:", err));

// Routes to manage files
app.get("/api/files", async (req, res) => {
  try {
    const files = await File.find();
    res.json(files);
  } catch (err) {
    console.error(err);
    res.status(500).send("Server Error");
  }
});

app.get("/api/files/:id", async (req, res) => {
  try {
    const file = await File.findById(req.params.id);
    if (!file) {
      return res.status(404).send("File not found");
    }
    res.json(file);
  } catch (err) {
    console.error(err);
    res.status(500).send("Server Error");
  }
});

app.put("/api/files/:id", async (req, res) => {
  try {
    const updatedFile = await File.findByIdAndUpdate(
      req.params.id,
      { content: req.body.content, lastModified: Date.now() },
      { new: true }
    );
    res.json(updatedFile);
    io.to(updatedFile._id.toString()).emit("fileUpdate", updatedFile);
  } catch (err) {
    console.error(err);
    res.status(500).send("Server Error");
  }
});

// Route to execute Python code
app.post("/api/execute", (req, res) => {
  const { code } = req.body;

  if (!code) {
    return res.status(400).json({ output: "No code provided." });
  }

  // Write the code to a temporary file
  const tempFilePath = "temp_code.py";

  fs.writeFile(tempFilePath, code, (err) => {
    if (err) {
      console.error("Error writing to temp file:", err);
      return res.status(500).json({ output: "Failed to write code to file." });
    }

    // Execute the temporary Python file
    exec(`python ${tempFilePath}`, (error, stdout, stderr) => {
      // Clean up the temporary file after execution
      fs.unlink(tempFilePath, (unlinkErr) => {
        if (unlinkErr) {
          console.error("Error deleting temp file:", unlinkErr);
        }
      });

      if (error) {
        console.error("Execution error:", error);
        return res.json({ output: stderr || error.message });
      }

      res.json({ output: stdout });
    });
  });
});

app.post("/api/files", async (req, res) => {
  try {
    const { name, createdBy } = req.body;
    const content = req.body.content || ""; // Ensure content is always an empty string if not provided

    if (!name || !createdBy) {
      return res.status(400).json({ error: "Name and createdBy are required." });
    }

    const newFile = new File({
      name,
      content, // Use the empty string for content if not provided
      createdBy,
    });

    await newFile.save();
    res.status(201).json(newFile); // Return the newly created file
  } catch (err) {
    console.error("Error creating file:", err);
    res.status(500).send("Server Error");
  }
});

// Route to delete a file
app.delete("/api/files/:id", async (req, res) => {
  try {
    const fileId = req.params.id;
    console.log("Deleting file with ID:", fileId); // Log to confirm the ID
    const file = await File.findByIdAndDelete(fileId);
    if (!file) {
      return res.status(404).json({ error: "File not found" });
    }
    res.status(200).json({ message: "File deleted successfully" });
  } catch (err) {
    console.error("Error deleting file:", err);
    res.status(500).send("Server Error");
  }
});

// Initialize PeerJS server
const peerServer = new PeerServer({
  path: "/peerjs",
  port: 9000, // Choose a port for PeerJS server
  cors: {
    origin: "http://localhost:3000", // Allow frontend to connect from this URL
    methods: ["GET", "POST"],
    allowedHeaders: ["Content-Type"],
    credentials: true,
  },
});

peerServer.on("connection", (id) => {
  console.log(`PeerJS connection established with ID: ${id}`);
});

io.on("connection", (socket) => {
  console.log("A user connected:", socket.id);

  // Listen for users joining a file's editing session
  socket.on("join", (fileId) => {
    socket.join(fileId);
    console.log(`User ${socket.id} joined file ${fileId}`);
  });

  // Listen for updates to the file content (real-time sync only)
  socket.on("updateFile", (data) => {
    // Broadcast the updated content to all users in the same room
    io.to(data.fileId).emit("fileUpdate", data);
  });

  // Handle user disconnect
  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
  });
});

// Serve static files (e.g., for React frontend)
app.use(express.static("public"));

// Start the server on port 5000
server.listen(5000, () => {
  console.log("Server is running on http://localhost:5000");
});
