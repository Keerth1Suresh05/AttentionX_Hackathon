from moviepy.editor import VideoFileClip

def crop_vertical(input_path, output_path, start, end):
    clip = VideoFileClip(input_path)

    try:
        subclip = clip.subclip(start, end)

        new_width = int(subclip.h * 9 / 16)

        cropped = subclip.crop(
            x_center=subclip.w / 2,
            width=new_width,
            height=subclip.h
        )

        cropped.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            verbose=False,
            logger=None
        )

    finally:
        clip.close()
        subclip.close()
