import { useState } from "react";
import { Helmet } from "react-helmet";
import "./App.css";

export default function App() {
  const [result, setResult] = useState();
  const [question, setQuestion] = useState();
  const [file, setFile] = useState();
  const [fileUploaded, setFileUploaded] = useState(false);

  const handleQuestionChange = (event: any) => {
    setQuestion(event.target.value);
  };

  const handleFileChange = (event: any) => {
    setFile(event.target.files[0]);
    setFileUploaded(true);
  };

  const handleSubmit = (event: any) => {
    event.preventDefault();

    const formData = new FormData();

    if (file) {
      formData.append("file", file);
    }
    if (question) {
      formData.append("question", question);
    }

    fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        setResult(data.result);
      })
      .catch((error) => {
        console.error("Error", error);
      });
  };

  return (
    <div className="appBlock">

          <header>
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
              <div>
                <a className="navbar-brand" href="/">
                  Chatbot LLM
                </a>
                <div className="collapse navbar-collapse" id="navbarNav">
                  <ul className="navbar-nav">
                    <li className="nav-item">
                      <a className="nav-link" href="#">
                        Home
                      </a>
                    </li>
                    <li className="nav-item">
                      <a className="nav-link" href="#">
                        Dashboard
                      </a>
                    </li>
                    <li className="nav-item">
                      <a className="nav-link" href="#">
                        Orders
                      </a>
                    </li>
                    <li className="nav-item">
                      <a className="nav-link" href="#">
                        Products
                      </a>
                    </li>
                    <li className="nav-item">
                      <a className="nav-link" href="#">
                        Customers
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </nav>
          </header>

        <main className="container">
          <div className="form-container">
          <form onSubmit={handleSubmit} className="form">
            <label className="questionLabel" htmlFor="question">
              Question:
            </label>
            <input
              className="questionInput"
              id="question"
              type="text"
              value={question}
              onChange={handleQuestionChange}
              placeholder="Ask your question here"
            />

            <br></br>
            <label className="fileLabel" htmlFor="file">
              Upload CSV file:
            </label>

            <input
              type="file"
              id="file"
              name="file"
              accept=".pdf, .docx, .csv, .txt"
              onChange={handleFileChange}
              className="fileInput"
            />

            <br></br>

            {/* Display a message if file is uploaded */}
            {fileUploaded && <p className="fileUploadedMessage">File Uploaded Successfully!</p>}

            <br></br>
            <button
              className="submitBtn"
              type="submit"
              disabled={!file || !question}
            >
              Submit
            </button>
          </form>
          <p className="resultOutput">Result: {result}</p>
          </div>
        </main>
    </div>
  );
}
