import { PredictionResult } from "@/types/prediction";

export const generateMockPredictions = (uploadedImages: File[]): PredictionResult[] => {
  const colors = ['Navy Blue', 'Crimson Red', 'Emerald Green', 'Golden Yellow', 'Royal Purple'];
  const patterns = ['Polka Dot', 'Striped', 'Floral', 'Geometric', 'Solid'];
  const categories = ['Dress', 'T-shirt', 'Blazer', 'Skirt', 'Jeans'];
  const sleeves = ['Full Sleeve', 'Half Sleeve', 'Sleeveless', '3/4 Sleeve', 'Cap Sleeve'];
  const necklines = ['Round Neck', 'V-Neck', 'Boat Neck', 'High Neck', 'Off Shoulder'];
  const fits = ['Regular Fit', 'Slim Fit', 'Loose Fit', 'Tailored', 'Oversized'];
  const occasions = ['Casual', 'Formal', 'Party', 'Office', 'Weekend'];
  const materials = ['Cotton', 'Silk', 'Polyester', 'Chiffon', 'Denim'];
  const seasons = ['Summer', 'Winter', 'Spring', 'Monsoon', 'All Season'];
  const styles = ['Contemporary', 'Traditional', 'Boho', 'Minimalist', 'Vintage'];

  return uploadedImages.map((file, index) => {
    const category = categories[Math.floor(Math.random() * categories.length)];
    return {
      id: index,
      name: file.name,
      category,   // ✅ Yeh alag field hai
      attributes: {
        color: colors[Math.floor(Math.random() * colors.length)],
        pattern: patterns[Math.floor(Math.random() * patterns.length)],
        sleeve: sleeves[Math.floor(Math.random() * sleeves.length)],
        neckline: necklines[Math.floor(Math.random() * necklines.length)],
        fit: fits[Math.floor(Math.random() * fits.length)],
        occasion: occasions[Math.floor(Math.random() * occasions.length)],
        material: materials[Math.floor(Math.random() * materials.length)],
        season: seasons[Math.floor(Math.random() * seasons.length)],
        style: styles[Math.floor(Math.random() * styles.length)]
      },
      imageUrl: URL.createObjectURL(file)
    };
  });
};
