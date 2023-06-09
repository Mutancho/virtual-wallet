import React, { useState, useEffect, useRef } from "react";
import "./ChatPage.css";
import Sidebar from "../SideBar/SideBar";
import { PrettyChatWindow } from "react-chat-engine-pretty";

const ChatsPage = (props) => {
    // const data = localStorage.getItem('props')
    // console.log(data)
    console.log(props)

  return (
      <div>
        <Sidebar />
    <div className="chat-window" style={{ height: "100vh", width: "82vw" ,marginLeft: "18vw"}}>
      <PrettyChatWindow
        projectId={'79d6fdad-378e-442a-98b8-fc49beb7e9c0'}
        username={props.user.info.username} // adam
        secret={props.user.pass} // pass1234
        style={{ height: "100%" }}
      />
    </div>
        </div>
  );
};

export default ChatsPage;








//
// function App() {
//   const [clientId, setClienId] = useState(
//     Math.floor(new Date().getTime() / 1000)
//   );
//
//   const [chatHistory, setChatHistory] = useState([]);
//   const [isOnline, setIsOnline] = useState(false);
//   const [textValue, setTextValue] = useState("");
//   const [websckt, setWebsckt] = useState();
//
//   const [message, setMessage] = useState([]);
//   const [messages, setMessages] = useState([]);
//
//   useEffect(() => {
//     const url = "ws://localhost:8000/ws/" + clientId;
//     const ws = new WebSocket(url);
//
//     ws.onopen = (event) => {
//       ws.send("Connect");
//     };
//
//     // recieve message every start page
//     ws.onmessage = (e) => {
//       const message = JSON.parse(e.data);
//       setMessages([...messages, message]);
//     };
//
//     setWebsckt(ws);
//     //clean up function when we close page
//     return () => ws.close();
//   }, [message,messages]);
//
//   const sendMessage = () => {
//     websckt.send(message);
//     // recieve message every send message
//     websckt.onmessage = (e) => {
//       const message = JSON.parse(e.data);
//       setMessages([...messages, message]);
//     };
//     setMessage([]);
//   };
//
//   return (
//     <div className="container">
//         <Sidebar />
//       <h1>Chat</h1>
//       <h2>Your client id: {clientId} </h2>
//       <div className="chat-container">
//         <div className="chat">
//           {messages.map((value, index) => {
//             if (value.clientId === clientId) {
//               return (
//                 <div key={index} className="my-message-container">
//                   <div className="my-message">
//                     <p className="client">client id : {clientId}</p>
//                     <p className="message">{value.message}</p>
//                   </div>
//                 </div>
//               );
//             } else {
//               return (
//                 <div key={index} className="another-message-container">
//                   <div className="another-message">
//                     <p className="client">client id : {clientId}</p>
//                     <p className="message">{value.message}</p>
//                   </div>
//                 </div>
//               );
//             }
//           })}
//         </div>
//         <div className="input-chat-container">
//           <input
//             className="input-chat"
//             type="text"
//             placeholder="Chat message ..."
//             onChange={(e) => setMessage(e.target.value)}
//             value={message}
//           ></input>
//           <button className="submit-chat" onClick={sendMessage}>
//             Send
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }
//
// export default App;