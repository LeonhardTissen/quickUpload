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

async function uploadFile(file, filename) {
	const formData = new FormData();
	console.log(file, filename);
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

async function upload() {
	let hasLargeFiles = false;
	for await (const file of uploadInput.files) {
		if (file.size > 100 * 1024 * 1024) {
			hasLargeFiles = true;

			const fileCount = Math.ceil(file.size / (100 * 1024 * 1024));
			const chunkSize = Math.ceil(file.size / fileCount);

			for (let i = 0; i < fileCount; i++) {
				const chunk = file.slice(i * chunkSize, (i + 1) * chunkSize);
				console.log(file.name);
				await uploadFile(chunk, `${file.name}.part${i + 1}`);
			}
		} else {
			await uploadFile(file);
		}
	}

	if (hasLargeFiles) await sendCombinerRequest();

	location.reload();
}
