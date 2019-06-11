export const exportJsonAsCsv = (rows) => {
  const csvContent = generateCsvString(rows);
  const encodedUri = "data:text/csv;charset=utf-8," + encodeURI(csvContent);
  window.open(encodedUri);

};

const generateCsvString = (rows) => {
  const headers = Object.keys(rows[0]).join(',');
  const lineArray = [headers];
  rows.forEach(function (infoArray) {
    const line = Object.values(infoArray).join(",");
    lineArray.push(line);
  });
  return lineArray.join("\n");
};
