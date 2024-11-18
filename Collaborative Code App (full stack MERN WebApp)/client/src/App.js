import React, { useState, useEffect } from "react";
import axios from "axios";
import FileEditor from "./components/FileEditor";
import VoiceCall from "./components/VoiceCall";
import "./App.css"; // Import the CSS file for styling

const App = () => {
  const [files, setFiles] = useState([]); // List of files from the database
  const [selectedFile, setSelectedFile] = useState(null); // The file currently being edited
  const [isVoiceCallActive, setIsVoiceCallActive] = useState(false);
  const [currentUserId, setCurrentUserId] = useState("user123"); // Dummy user ID for testing
  const [executionOutput, setExecutionOutput] = useState(""); // Store Python code execution output
  const [newFileName, setNewFileName] = useState(""); // New file name input

  // Fetch list of files from the backend (database)
  useEffect(() => {
    axios
      .get("http://localhost:5000/api/files")
      .then((response) => {
        setFiles(response.data);
      })
      .catch((err) => console.error(err));
  }, []);

  // Handle file selection for editing
  const handleFileSelect = (fileId) => {
    // Get the file data from the server
    axios
      .get(`http://localhost:5000/api/files/${fileId}`)
      .then((response) => {
        setSelectedFile(response.data); // Set the selected file to state
      })
      .catch((err) => console.error(err));
  };

  // Handle file content update after editing (e.g., save button pressed)
  const handleFileUpdate = (updatedFile) => {
    axios
      .put(`http://localhost:5000/api/files/${updatedFile._id}`, {
        content: updatedFile.content,
      })
      .then((response) => {
        setSelectedFile(response.data); // Update the file content in state
        console.log("File updated:", response.data);
      })
      .catch((err) => console.error("Error updating file:", err));
  };

  // Execute Python Code
  const executePythonCode = () => {
    if (selectedFile && selectedFile.content) {
      axios
        .post("http://localhost:5000/api/execute", { code: selectedFile.content })
        .then((response) => {
          setExecutionOutput(response.data.output);
        })
        .catch((err) => {
          setExecutionOutput("Error executing code.");
          console.error(err);
        });
    } else {
      setExecutionOutput("No code to execute.");
    }
  };

  // Create a new file
  const handleCreateFile = () => {
    const newFileName = prompt("Enter a name for the new file:");
    if (newFileName) {
      const newFile = {
        name: newFileName,
        content: "", // New file should start with empty content
        createdBy: currentUserId, // Add the current user ID as the creator
      };
  
      axios
        .post("http://localhost:5000/api/files", newFile)
        .then((response) => {
          setFiles((prevFiles) => [...prevFiles, response.data]);
          alert("New file created!");
        })
        .catch((err) => {
          console.error("Error creating file: ", err);
          alert("Error creating file.");
        });
    }
  };

  // Delete a file
  const handleDeleteFile = (fileId) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this file?");
    if (confirmDelete) {
      axios
        .delete(`http://localhost:5000/api/files/${fileId}`)
        .then(() => {
          setFiles(files.filter((file) => file._id !== fileId)); // Remove the deleted file from the list
          if (selectedFile && selectedFile._id === fileId) {
            setSelectedFile(null); // If the deleted file is the one being edited, clear the selected file
          }
          alert("File deleted successfully!");
        })
        .catch((err) => {
          console.error("Error deleting file:", err);
          alert("Error deleting file.");
        });
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">Collaborative Text Editor</h1>
      <div className="content-wrapper">
        {/* File Selector Section */}
        <div className="file-selector card">
          <h2>Choose a file to edit:</h2>
          {files.length > 0 ? (
            <ul className="file-list">
              {files.map((file) => (
                <li key={file._id}>
                  <button
                    className="file-button"
                    onClick={() => handleFileSelect(file._id)}
                  >
                    {file.name}
                  </button>
                  {/* Add delete button */}
                  <button
                    className="delete-button"
                    onClick={() => handleDeleteFile(file._id)}
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p>No files found</p>
          )}
          {/* New File Creation Section */}
          <div className="create-file">
            <button onClick={handleCreateFile}>Create New File</button>
          </div>
        </div>

        {/* Voice Call Section */}
        <div className="voice-call card">
          <VoiceCall
            isActive={isVoiceCallActive}
            setIsVoiceCallActive={setIsVoiceCallActive}
          />
        </div>

        {/* Collaborative Text Editor Section */}
        <div className="text-editor card">
          {selectedFile ? (
            <>
              <FileEditor
                file={selectedFile} // Make sure the file prop updates
                setFile={setSelectedFile} // Ensure this is being called to update content in the parent
                currentUserId={currentUserId}
                handleFileUpdate={handleFileUpdate} // Pass the handleFileUpdate function to save changes
              />
              <button className="save-button" onClick={executePythonCode}>
                Run Code
              </button>
              <div className="execution-output">
                <h2 className="execHeader">Execution Output:</h2>
                <pre>{executionOutput}</pre>
              </div>
            </>
          ) : (
            <p>Select a file to start editing.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
