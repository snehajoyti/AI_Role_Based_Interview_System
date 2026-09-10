import { useState } from "react";

function App() {
  const [resume, setResume] = useState(null);
  const [role, setRole] = useState("");
  const [message, setMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [resumeProfile, setResumeProfile] = useState(null);
  const [questionNumber, setQuestionNumber] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [interviewStarted, setInterviewStarted] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const [summary, setSummary] = useState("");

  const handleViewSummary = async () => {
    if (!sessionId) return;

    setMessage("Generating final interview summary...");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/interview/summary/${sessionId}`
      );

      if (!response.ok) {
        throw new Error("Summary generation failed.");
      }
      const data = await response.json();

      setSummary(data.summary);
      setShowSummary(true);
      setMessage("Final interview summary generated successfully.");
    } catch (error) {
      console.error(error);
      setMessage("Something went wrong while generating the summary.");
    }
  };
   
  const handleResumeChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      setResume(file);
      setMessage(`Resume selected: ${file.name}`);
    }
  };

  const handleSubmitAnswer = async () => {
    if (isSubmitting) return;

    setIsSubmitting(true);

    if (!answer.trim()) {
      setMessage("Please enter your answer.");
      setIsSubmitting(false);
      return;
    }

    setMessage("Submitting answer...");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/interview/answer",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
             session_id: sessionId,
             question: question,
             answer: answer,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Answer submission failed.");
      }

      await response.json();

      setMessage("Generating next interview question...");

      const nextQuestionResponse = await fetch(
        "http://127.0.0.1:8000/interview/generate-question",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            role: role,
            resume_profile: resumeProfile,
            topic: "Machine Learning",
          }),
        }
      );

      if (!nextQuestionResponse.ok) {
        throw new Error("Next question generation failed.");
      }

      const nextQuestionData = await nextQuestionResponse.json();

      console.log("NEXT QUESTION DATA:", nextQuestionData);

      setQuestion(nextQuestionData.question);
      setQuestionNumber((prev) => prev + 1);
      setAnswer("");
      setMessage("Next interview question generated successfully.");
    } catch (error) {
      console.error(error);
      setMessage("Something went wrong while submitting the answer.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleStartInterview = async () => {
    if (interviewStarted) return;

    if (!resume) {
      setMessage("Please upload your resume first.");
      return;
    }

    if (!role) {
      setMessage("Please select a target role.")
      return;
    }

    setMessage("Uploading resume...");


    try {
      // Upload Resume
      const formData = new FormData();
      formData.append("file", resume);

      const resumeResponse = await fetch(
        "http://127.0.0.1:8000/resume/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!resumeResponse.ok) {
        throw new Error("Resume upload failed.");
      }

      const resumeData = await resumeResponse.json();

      setResumeProfile(resumeData.profile);

      console.log("RESUME DATA:",resumeData);
      console.log("RESUME TEXT:", resumeData.text);
      console.log("RESUME TEXT LENGTH:", resumeData.text?.length);

      //Start Interview Session
      const startResponse = await fetch(
        "http://127.0.0.1:8000/interview/start",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            role: role,
            resume_text: resumeData.resume_text,
          }),
        }
      );
      if (!startResponse.ok) {
        const errorData = await startResponse.json();
        console.log("START INTERVIEW  ERROR:", errorData);
        throw new Error(
          errorData.detail 
            ? JSON.stringify(errorData.detail)
            : "Interview session start failed."
        );
      }

      const startData = await startResponse.json();

      setSessionId(startData.session_id);
      setInterviewStarted(true);

      //Send role + resume profile to backend
      const roleResponse = await fetch(
        "http://127.0.0.1:8000/interview/select-role",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            role:role,
            resume_profile: resumeData.profile,
          }),
        }
      );

      if (!roleResponse.ok) {
        throw new Error("Role selection failed.");
      }

      await roleResponse.json();

      // Generate first interview question
      setMessage("Generating interview question...");

      const questionResponse = await fetch(
        "http://127.0.0.1:8000/interview/generate-question",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          }, 
          body: JSON.stringify({
            role: role,
            resume_profile: resumeData.profile,
            topic: "Machine Learning",
          }),
        }
      );

      if (!questionResponse.ok) {
        throw new Error("Question generation failed.");
      }
      const questionData = await questionResponse.json();

      console.log("QUESTION DATA:", questionData);
      console.log("GENERATED QUESTION:", questionData.question);

      setQuestion(questionData.question);
      setMessage("Interview question generated successfully.");


    } catch (error) {
      console.error(error);
      setMessage("Something went wrong while submitting the answer.");
    } 
  };

  return (
    <div 
      style={{
        minHeight: "100vh",
        backgroundColor: "#f5f7fb",
        padding: "40px 20px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          maxWidth: "800px",
          margin: "0 auto",
          backgroundColor: "white",
          padding: "40px",
          borderRadius: "16px",
          boxShadow: "0 4px 20px rgba(0,0,0,08)",
        }}
      >
        <h1 style={{ textAlign: "center", marginBottom: "10px"}}>
          AI Role-Based Interview System
        </h1>

        <p
          style={{
            textAlign: "center",
            color: "#666",
            marginBottom: "35px",
          }}
        >
          Upload your resume and select a target role to begin your AI-Powered
          technical interview.
        </p>

        <div style={{ marginBottom: "30px" }}>
          <h2>1. Upload Resume</h2>

          <input
            type="file"
            onChange={handleResumeChange}
            />

            {resume && (
              <p style={{ color: "green", marginTop: "10px" }}>
                  {resume.name}
              </p>
            )}
      </div>

      <div style={{ marginBottom: "30px "}}>
        <h2>2. Select Target Role</h2>

        <select
          value={role}
          onChange={(event) => setRole(event.target.value)}
          style={{
            width: "100%",
            padding: "12px",
            fontSize: "16px",
            borderRadius: "8px",
            border: "1px solid #ccc",
          }}
        >
          <option value="">Select a role</option>
          <option value="AI/ML Engineer">AI/ML Engineer</option>
          <option value="Data Scientist">Data Scientist</option>
        </select>
      </div>

      <button 
        onClick={handleStartInterview}
        disabled={interviewStarted}
        style={{
          width: "100%",
          padding: "14px",
          fontSize: "17px",
          fontWeight: "bold",
          color: "white",
          backgroundColor: "#646cff",
          border: "none",
          borderRadius: "8px",
          cursor: interviewStarted ? "not-allowed" : "pointer",
        }}
      >
        Start Interview 
      </button>

      {message && (
        <p 
          style={{
            marginTop: "20px",
            textAlign: "center",
            fontWeight: "bold",
          }}
        >
          {message}
        </p>
      )}

            {interviewStarted && (
        <div
          style={{
            marginTop: "30px",
            padding: "20px",
            backgroundColor: "#f0f2ff",
            borderRadius: "10px",
          }}
        >
          <h2>Interview Question {questionNumber}</h2>

          <p style={{ fontSize: "18px", lineHeight: "1.6" }}>
            {question}
          </p>

          <textarea
            value={answer}
            onChange={(event) => setAnswer(event.target.value)}
            placeholder="Type your answer here..."
            rows="6"
            style={{
              width: "100%",
              padding: "12px",
              fontSize: "16px",
              borderRadius: "8px",
              border: "1px solid #ccc",
              marginTop: "15px",
              boxSizing: "border-box",
              resize: "vertical",
            }}
          />

          <button 
            onClick={handleSubmitAnswer}
            disabled={isSubmitting}
            style={{
              marginTop: "15px",
              padding: "12px",
              fontSize: "16px",
              fontWeight: "bold",
              color: "white",
              backgroundColor: "#28a745",
              border: "none",
              borderRadius: "8px",
              cursor: isSubmitting ? "not-allowed" : "pointer",
            }}
            >
              {isSubmitting ? "Submitting..." : "Submit Answer"}
            </button>

            <button
              onClick={handleViewSummary}
              style={{
                marginTop: "15px",
                marginLeft: "10px",
                padding: "12px",
                fontSize: "16px",
                fontWeight: "bold",
                color: "white",
                backgroundColor: "#646cff",
                border: "none",
                borderRadius: "8px",
                cursor: "pointer",
              }}
            >
              View Final Summary 
            </button>

            {showSummary && (
              <div 
              style={{
                marginTop: "30px",
                padding: "25px",
                backgroundColor: "#f8f9ff",
                borderRadius: "10px",
                border: "1px solid #dfe3ff",
                textAlign: "left",
              }}
            >
              <h2>Final Interview Summary</h2>

              <pre
                style={{
                  whiteSpace: "pre-wrap",
                  fontFamily: "Arial, sans-serif",
                  fontSize: "16px",
                  lineHeight: "1.6",
                }}
              >
                {summary}
              </pre>
            </div> 
            )}
        </div>
      )}
    </div>
    </div>
  );
}

export default App;
