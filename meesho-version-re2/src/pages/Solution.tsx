
import { useState, useCallback } from 'react';
import { PredictionResult } from '@/types/prediction';
import { generateMockPredictions, downloadCSV, downloadPDF } from '@/utils/predictionService';
import SolutionNavigation from '@/components/solution/SolutionNavigation';
import SolutionHero from '@/components/solution/SolutionHero';
import FileUploadSection from '@/components/solution/FileUploadSection';
import LoadingAnimation from '@/components/solution/LoadingAnimation';
import ResultsSection from '@/components/solution/ResultsSection';

const Solution = () => {
  const [uploadedImages, setUploadedImages] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [predictions, setPredictions] = useState<PredictionResult[]>([]);
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);

  const handleFileUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    console.log('File upload triggered');
    const files = Array.from(event.target.files || []);
    console.log('Files selected:', files.length);
    
    const validFiles = files.filter(file => file.type.startsWith('image/'));
    console.log('Valid image files:', validFiles.length);
    
    if (validFiles.length > 10) {
      alert('Maximum 10 images allowed');
      return;
    }
    
    setUploadedImages(prev => {
      const newImages = [...prev, ...validFiles].slice(0, 10);
      console.log('Updated uploaded images:', newImages.length);
      return newImages;
    });
    setPredictions([]);
    setSelectedImageIndex(0);
    
    // Clear the input value to allow selecting the same files again
    event.target.value = '';
  }, []);

  const handleRemoveImage = useCallback((index: number) => {
    setUploadedImages(prev => prev.filter((_, i) => i !== index));
    setPredictions([]);
    setSelectedImageIndex(0);
  }, []);

  const analyzeImages = async () => {
    console.log('Analyze button clicked, images:', uploadedImages.length);
    if (uploadedImages.length === 0) return;
    
    setIsProcessing(true);
    
    // Simulate AI processing with 5-second delay
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    const mockPredictions = generateMockPredictions(uploadedImages);
    console.log('Generated predictions:', mockPredictions.length);
    setPredictions(mockPredictions);
    setSelectedImageIndex(0);
    setIsProcessing(false);
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
