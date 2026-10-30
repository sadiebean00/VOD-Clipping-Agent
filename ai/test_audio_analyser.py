from ai.audio_analyser import analyse_audio

video_path = "data/downloads/project_3.mp4"
print(f"Testing file: {video_path}")

results = analyse_audio(video_path)

print("\nAudio Analysis Complete!")
print(f"Audio frames analysed: {len(results['energy'])}")
print(f"Duration analysed: {results['timestamps'][-1]:.2f} seconds")
print(f"Highest audio energy: {max(results['energy']):.4f}")