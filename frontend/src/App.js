import { useState } from "react";
import Header from "./components/Header";
import Register from "./components/Register";
import Login from "./components/Login";
import Profile from "./components/Profile";
import ItemManagement from "./components/ItemManagement";
import SubmissionManagement from "./components/SubmissionManagement";

function App() {
  const [page, setPage] = useState("home");

  const handleLoginSuccess = () => {
    setPage("profile");
  };

  return (
    <div className="App">
      <Header />
      {page === "home" && (
        <div>
          <button onClick={() => setPage("login")}>Login</button>
          <button onClick={() => setPage("register")}>Register</button>
        </div>
      )}
      {page === "login" && <Login onLoginSuccess={handleLoginSuccess} />}
      {page === "register" && <Register />}
      {page === "profile" && (
        <div>
          <Profile />
          <button onClick={() => setPage("items")}>Manage Items</button>
          <button onClick={() => setPage("submissions")}>Manage Submissions</button>
        </div>
      )}
      {page === "items" && <ItemManagement />}
      {page === "submissions" && <SubmissionManagement />}
    </div>
  );
}

export default App;