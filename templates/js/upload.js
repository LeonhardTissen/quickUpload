const uploadButton = document.getElementById('uploadbutton');
const uploadInput = document.getElementById('file');

uploadButton.addEventListener('click', () => {
	uploadInput.click();
});

document.body.addEventListener('dragover', (e) => {
	e.preventDefault();
});

document.body.addEventListener('drop', (e) => {
	e.preventDefault();
	uploadInput.files = e.dataTransfer.files;
	upload();
});

uploadInput.addEventListener('input', upload);

function upload() {
	// Post request to /upload
	const formData = new FormData();
	// Add all files
	for (const file of uploadInput.files) {
		if (file.size > 100 * 1024 * 1024) {
			// If over 100MB, split into chunks
			const fileCount = Math.ceil(file.size / (100 * 1024 * 1024));
			const chunkSize = Math.ceil(file.size / fileCount);

			for (let i = 0; i < fileCount; i++) {
				const chunk = file.slice(i * chunkSize, (i + 1) * chunkSize);
				formData.append('file', chunk, file.name + '.part' + i);
			}
		} else {
			formData.append('file', file);
		}
	}

	fetch('/upload', {
		method: 'POST',
		body: formData,
	}).then(() => {
		location.reload();
	});
}
