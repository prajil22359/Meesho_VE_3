
import { useState, useCallback } from "react";
import { PredictionResult } from "@/types/prediction";
import { downloadCSV, downloadPDF } from "@/utils/predictionService";
import SolutionNavigation from "@/components/solution/SolutionNavigation";
import SolutionHero from "@/components/solution/SolutionHero";
import FileUploadSection from "@/components/solution/FileUploadSection";
import LoadingAnimation from "@/components/solution/LoadingAnimation";
import ResultsSection from "@/components/solution/ResultsSection";

const Solution = () => {
  const [uploadedImages, setUploadedImages] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [predictions, setPredictions] = useState<PredictionResult[]>([]);
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);

  const handleFileUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    const validFiles = files.filter((file) => file.type.startsWith("image/"));
    if (validFiles.length > 10) {
      alert("Maximum 10 images allowed");
      return;
    }

    setUploadedImages((prev) => {
      const newImages = [...prev, ...validFiles].slice(0, 10);
      return newImages;
    });

    setPredictions([]);
    setSelectedImageIndex(0);
    event.target.value = "";
  }, []);

  const handleRemoveImage = useCallback((index: number) => {
    setUploadedImages((prev) => prev.filter((_, i) => i !== index));
    setPredictions([]);
    setSelectedImageIndex(0);
  }, []);

  const analyzeImages = async () => {
    if (uploadedImages.length === 0) return;
    setIsProcessing(true);

    const formData = new FormData();
    formData.append("image", uploadedImages[0]);

    try {
      const res = await fetch("http://localhost:8000/api/predict/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      console.log("Backend prediction response:", data);

      // Format into PredictionResult type
      const formattedPrediction: PredictionResult = {
        id: Date.now(),
        name: uploadedImages[0].name,
        imageUrl: URL.createObjectURL(uploadedImages[0]),
        confidence: data.prediction.confidence || 0,
        attributes: {
          color: data.prediction.color || "Unknown",
          pattern: data.prediction.pattern || "Unknown",
          category: data.prediction.category || "Unknown",
          sleeve: data.prediction.sleeve || "Unknown",
          neckline: data.prediction.neckline || "Unknown",
          fit: data.prediction.fit || "Unknown",
          occasion: data.prediction.occasion || "Unknown",
          material: data.prediction.material || "Unknown",
          season: data.prediction.season || "Unknown",
          style: data.prediction.style || "Unknown",
        },
      };

      setPredictions([formattedPrediction]);
      setSelectedImageIndex(0);
    } catch (error) {
      console.error("Error calling prediction API:", error);
      alert("An error occurred while analyzing the image.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownloadCSV = () => {
    downloadCSV(predictions);
  };

  const handleDownloadPDF = () => {
    downloadPDF();
  };

  const handleStartNew = () => {
    setUploadedImages([]);
    setPredictions([]);
    setSelectedImageIndex(0);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-white">
      <SolutionNavigation />
      <div className="container mx-auto px-6 py-12">
        <SolutionHero />

        {!predictions.length && !isProcessing && (
          <FileUploadSection
            uploadedImages={uploadedImages}
            onFileUpload={handleFileUpload}
            onAnalyze={analyzeImages}
            onRemoveImage={handleRemoveImage}
          />
        )}

        {isProcessing && <LoadingAnimation />}

        {predictions.length > 0 && !isProcessing && (
          <ResultsSection
            predictions={predictions}
            selectedImageIndex={selectedImageIndex}
            onImageSelect={setSelectedImageIndex}
            onDownloadPDF={handleDownloadPDF}
            onDownloadCSV={handleDownloadCSV}
            onStartNew={handleStartNew}
          />
        )}
      </div>
    </div>
  );
};

export default Solution;
