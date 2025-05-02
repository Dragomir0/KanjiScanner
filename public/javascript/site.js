(() => {
  document.addEventListener("DOMContentLoaded", () => {

    // Remove last line button
    document.getElementById("undoButton").addEventListener("click", () => {
      const lines = document.getElementsByTagName("p");
      if (lines.length > 0) {
        const lastLine = lines[lines.length - 1];
        lastLine.remove();

      }
    });

    // Clear all lines button
    document.getElementById("clearButton").addEventListener("click", () => {
      const linesToRemove = document.getElementsByTagName("p");

      if (linesToRemove.length > 0) {
        Array.from(linesToRemove).forEach((line) => {
          document.querySelector("body").removeChild(line);
        });
        document.querySelector("#counter").textContent = "0";
      };
    });
  });
})();