import React, { useState, useEffect } from "react";
import Peer from "peerjs";

const VoiceCall = ({ isActive, setIsVoiceCallActive }) => {
  const [peer, setPeer] = useState(null);
  const [stream, setStream] = useState(null);
  const [peerId, setPeerId] = useState(""); // Store this peer's ID
  const [isReady, setIsReady] = useState(false); // Track if both peer and stream are ready

  useEffect(() => {
    console.log("Initializing PeerJS and media...");
  
    const peerInstance = new Peer({
      host: "localhost",
      port: 9000,
      path: "/peerjs",
      secure: false, // Use true if you're using HTTPS
      debug: 3
    });
  
    peerInstance.on("open", (id) => {
      console.log("Peer ID assigned:", id);
      setPeerId(id);  // Set the peer ID for this user
      setPeer(peerInstance);  // Ensure that peer is set after ID is assigned
    });
  
    // Get the user's media (audio)
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((audioStream) => {
        console.log("Audio stream initialized:", audioStream);
        setStream(audioStream);  // Set the local stream
  
        // Listen for incoming calls
        peerInstance.on("call", (incomingCall) => {
          console.log("Incoming call received:", incomingCall);
          incomingCall.answer(audioStream);  // Answer the call with the local stream
  
          incomingCall.on("stream", (remoteStream) => {
            console.log("Incoming remote stream received:", remoteStream);
            const audio = new Audio();
            audio.srcObject = remoteStream;
            audio.play();
          });
        });
  
        // Set readiness once both peer and stream are ready
        setIsReady(true);
        console.log("PeerJS and audio stream are ready.");
      })
      .catch((err) => {
        console.error("Failed to access user media:", err);
      });
  
    // Cleanup function when component unmounts
    return () => {
      peerInstance.destroy();
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);  // Empty dependency array ensures this runs only once when the component mounts

  const startCall = () => {
    console.log("Starting call: Peer Ready?", !!peer, "Stream Ready?", !!stream);

    // Check if peer and stream are both ready
    if (!isReady) {
      alert("Unable to start call. Ensure PeerJS and audio stream are initialized.");
      return;
    }

    if (!peer || !stream) {
        alert("Unable to start call. Ensure PeerJS and audio stream are initialized.");
        return;
    }

    // Ask for the peer ID to call
    const targetPeerId = prompt("Enter the ID of the peer to call:");
    if (targetPeerId) {
      console.log("Attempting to call peer:", targetPeerId);
      const outgoingCall = peer.call(targetPeerId, stream);  // Start the call

      outgoingCall.on("stream", (remoteStream) => {
        console.log("Outgoing call connected. Remote stream received:", remoteStream);
        const audio = new Audio();
        audio.srcObject = remoteStream;
        audio.play();
      });

      outgoingCall.on("close", () => {
        console.log("Call ended.");
      });
    }
  };

  return (
    <div>
      <h2>Your Call ID:</h2>
      <p className="peerId">{peerId}</p>
      {isActive ? (
        <div>
          <button onClick={() => setIsVoiceCallActive(false)}>End Call</button>
        </div>
      ) : (
        <button
          className="voice-button"
          onClick={startCall}
          disabled={!isReady}  // Disable button if peer or stream is not ready
        >
          Connect to Call
        </button>
        
      )}
    </div>
  );
};

export default VoiceCall;
