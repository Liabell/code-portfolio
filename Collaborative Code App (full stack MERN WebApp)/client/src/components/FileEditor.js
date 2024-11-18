import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import axios from "axios";
import ReactCodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python'; // Import Python language for CodeMirror

const FileEditor = ({ file, setFile, currentUserId }) => {
  const [content, setContent] = useState(file.content); // Local content state
  const [socket, setSocket] = useState(null); // Socket connection state

  useEffect(() => {
    // If no file is provided, do nothing
    if (!file) return;

    // Initialize the socket connection
    const socketInstance = io("http://localhost:5000");
    setSocket(socketInstance);

    // Join a room with the file ID to start collaborative editing
    socketInstance.emit("join", file._id);

    // Listen for updates to the file's content from other users
    socketInstance.on("fileUpdate", (updatedContent) => {
      if (updatedContent.fileId === file._id && updatedContent.content !== content) {
        setContent(updatedContent.content); // Update local content with synced changes
      }
    });

    // Cleanup socket connection when the component is unmounted
    return () => {
      socketInstance.disconnect();
    };
  }, [file]); // Run only when file changes

  useEffect(() => {
    // When the selected file changes, update the content state
    setContent(file.content);
  }, [file]);

  // Handle local content changes
  const handleContentChange = (value) => {
    setContent(value); // Update local state
    if (socket) {
      socket.emit("updateFile", { fileId: file._id, content: value }); // Broadcast changes
    }
  };

  // Save file to the database
  const handleSave = () => {
    axios
      .put(`http://localhost:5000/api/files/${file._id}`, { content })
      .then((response) => {
        alert("File saved successfully!");
        setFile(response.data); // Update the parent file state
      })
      .catch((err) => {
        console.error("Error saving file:", err);
      });
  };

  return (
    <div>
      <p className="fileName">{file.name}</p>
      <br />
      <ReactCodeMirror
        value={content} // CodeMirror editor content bound to local state
        onChange={(value) => handleContentChange(value)} // Handle content changes
        extensions={[python()]} // Enable Python syntax highlighting
        height="400px" // Set the editor height
        theme="light" // Optional: You can set a theme (light/dark)
      />
      <br />
      <button className="save-button" onClick={handleSave}>Save Changes</button>
    </div>
  );
};

export default FileEditor;
