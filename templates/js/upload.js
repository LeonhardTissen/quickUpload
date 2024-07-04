const uploadButton = document.getElementById('uploadbutton');
const uploadInput = document.getElementById('file');

let uploadLock = false;

uploadButton.addEventListener('click', () => {
	if (uploadLock) return;

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

// Prevent closing the tab when uploading
window.addEventListener('beforeunload', (e) => {
	if (uploadLock) {
		e.preventDefault();
	}
});

uploadInput.addEventListener('input', upload);

async function uploadFile(file, filename) {
	const formData = new FormData();
	formData.append('file', file, filename);

	await fetch('/upload', {
		method: 'POST',
		body: formData,
	});
}

async function sendCombinerRequest() {
	await fetch('/combine', {
		method: 'POST',
	});
}

let maxChunkSize = 80 * 1024 * 1024; // 80MB

let chunksFinished = 0;
let totalChunks = 0;

function addFinishedChunk() {
	chunksFinished++;
	updateText();
}

function updateText() {
	let percentage = Math.round((chunksFinished / totalChunks) * 100);
	if (isNaN(percentage)) percentage = 0;
	uploadButton.innerText = `Uploading... (${percentage}%)`;
	uploadButton.style.background = `linear-gradient(
		90deg,
		var(--color-low) ${percentage}%,
		#FFF4 ${percentage}%
	)`;
}

async function upload() {
	if (uploadLock) return;
	uploadLock = true;

	const files = uploadInput.files;

	updateText();

	for await (const file of files) {
		if (file.size > maxChunkSize) {
			const fileCount = Math.ceil(file.size / maxChunkSize);
			totalChunks += fileCount;
		} else {
			totalChunks++;
		}
	}

	let hasLargeFiles = false;
	for await (const file of files) {
		if (file.size > maxChunkSize) {
			hasLargeFiles = true;

			const fileCount = Math.ceil(file.size / maxChunkSize);
			const chunkSize = Math.ceil(file.size / fileCount);

			for (let i = 0; i < fileCount; i++) {
				const chunk = file.slice(i * chunkSize, (i + 1) * chunkSize);
				await uploadFile(chunk, `${file.name}.part${i + 1}`);
				addFinishedChunk();
			}
		} else {
			await uploadFile(file);
			addFinishedChunk();
		}
	}

	if (hasLargeFiles) await sendCombinerRequest();

	uploadLock = false;

	location.reload();
}
