class Bundler:
	def __init__(self):
		self._writer = ""
		self.sources = []

	def _write(self, text: str):
		self.sources.append(text)

	def from_file(self, filepath: str):
		with open(filepath, "r") as file:
			self._write(file.read())

	def from_source(self, source_code: str):
		self._write(source_code)

	def from_files(self, filepaths: list[str]):
		for f in filepaths:
			self.from_file(f)

	def bundle(self, cache=False):
		writer = self._writer
		for source in self.sources:
			writer += source + "\n\n"
		if cache:
			self._writer = writer
			self.sources = []
		return writer

	def get_bundled(self):
		return self.bundle(cache=False)

	def save_to(self, filepath: str):
		with open(filepath, "w") as file:
			file.write(self.get_bundled())