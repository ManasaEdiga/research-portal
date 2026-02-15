import { useEffect, useState } from "react";
import { uploadFile, getDocuments, runSummary, getSummary } from "./api";

export default function App() {
  const [docs, setDocs] = useState([]);
  const [summary, setSummary] = useState(null);

  const loadDocs = async () => {
    const data = await getDocuments();
    setDocs(data);
  };

  useEffect(() => {
    loadDocs();
  }, []);

  const handleUpload = async (file) => {
    await uploadFile(file);
    loadDocs();
  };

  const handleSummary = async (id) => {
    await runSummary(id);
    const res = await getSummary(id);
    setSummary(res.summary);
  };

  return (
    <div className="d-flex flex-column justify-content-center align-items-center text-center" style={{ padding: 20, fontFamily: "Times of New Roman", background: "linear-gradient(135deg, #c8f8ba 0%, #f5a0a0 50%, #b4e7f5 100%)", height: "100vh", width: "100%", textAlign: "center", flex: "row",justifyContent: "center" }}>
      <h1>Research Portal</h1>

      <h2>Upload Concall Transcript</h2>
      <input type="file" onChange={e => handleUpload(e.target.files[0])} />

      <h2>Concalls</h2>
      {docs.map(d => (
        <div key={d.id} style={{ marginBottom: 8 }}>
          {d.filename}
          <button
            style={{ marginLeft: 10 }}
            onClick={() => handleSummary(d.id)}
          >
            AI Summary
          </button>
        </div>
      ))}

      {summary && (
        <>
          <h2>AI Summary</h2>
          <pre style={{ background: "#f5f5f5", padding: 12 }}>
            {summary}
          </pre>
        </>
      )}
    </div>
  );
}
