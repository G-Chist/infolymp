function deleteNote(noteId) {
  fetch("/delete-note", { method: "POST", body: JSON.stringify({ noteId: noteId }),}).then((_res) => {window.location.href = "/task1";});
}
function deleteNote2(noteId) {
  fetch("/delete-note2", { method: "POST", body: JSON.stringify({ noteId: noteId }),}).then((_res) => {window.location.href = "/task2";});
}