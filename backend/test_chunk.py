from app.utils.chunker import chunk_text

sample_text = """
This is a test transcript.
""" * 500

chunks = chunk_text(sample_text)

print("Chunks:", len(chunks))

for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i}")
    print(chunk[:100])