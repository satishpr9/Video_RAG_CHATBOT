def extract_hook(segments, max_seconds=5):

    hook_parts = []

    for segment in segments:

        start = segment["start"]

        if start <= max_seconds:
            hook_parts.append(
                segment["text"].strip()
            )

    return " ".join(hook_parts)