import React, { useState } from "react";
import { motion } from "framer-motion";
import { Upload, FileText, ChevronDown, ChevronUp } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function InvoiceAuditAgent() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showJson, setShowJson] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setResponse(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("https://0ls2c319kd.execute-api.us-east-1.amazonaws.com/invoice/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      alert("Error contacting AI backend");
    }

    setLoading(false);
  };

  const statusColors = {
    AUTO_APPROVE: "bg-green-600",
    NEEDS_REVIEW: "bg-yellow-500",
    REJECT: "bg-red-600",
  };

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">

      {/* HEADER */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-4xl font-bold">Invoice Audit AI Agent</h1>
        <p className="text-gray-600 mt-2 text-lg">
          Upload an invoice and let AI validate, analyze, and generate a compliance-ready explanation.
        </p>
      </motion.div>

      {/* UPLOAD CARD */}
      <Card className="shadow-xl border rounded-2xl">
        <CardContent className="p-6 space-y-4">

          <div className="flex items-center gap-4">
            <Upload className="w-10 h-10 text-blue-600" />

            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files[0])}
              className="border p-2 rounded-lg w-full"
            />
          </div>

          <Button
            className="w-full mt-2"
            onClick={handleUpload}
            disabled={loading}
          >
            {loading ? "Processing..." : "Upload & Analyze Invoice"}
          </Button>
        </CardContent>
      </Card>

      {/* ANALYSIS RESULT */}
      {response && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-6"
        >

          {/* STATUS + SCORE */}
          <Card className="shadow-lg border rounded-2xl">
            <CardContent className="p-6 space-y-4">

              {/* Status Badge */}
              <div className="flex items-center justify-between">
                <span className="font-semibold text-xl flex items-center gap-2">
                  <FileText className="w-5 h-5 text-blue-600" />
                  AI Audit Result
                </span>

                <span className={`px-4 py-2 text-white rounded-full ${statusColors[response.final_status]}`}>
                  {response.final_status}
                </span>
              </div>

              {/* Risk Score */}
              <div className="text-lg">
                <span className="font-semibold">Risk Score:</span>{" "}
                {response.risk_score}
              </div>

              {/* Explanation */}
              <div className="mt-4 bg-gray-50 border rounded-xl p-4 whitespace-pre-wrap leading-relaxed">
                {response.explanation}
              </div>
            </CardContent>
          </Card>

          {/* RAW JSON RESPONSE */}
          <Card className="shadow-lg border rounded-2xl">
            <CardContent className="p-6 space-y-4">

              <Button
                variant="outline"
                className="w-full flex items-center justify-between"
                onClick={() => setShowJson(!showJson)}
              >
                <span>Show AI Full Response (JSON)</span>
                {showJson ? <ChevronUp /> : <ChevronDown />}
              </Button>

              {showJson && (
                <pre className="mt-4 bg-black text-green-400 p-4 rounded-xl overflow-auto text-sm max-h-96">
{JSON.stringify(response, null, 2)}
                </pre>
              )}

            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
