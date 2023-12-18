class RGBColorConverter:
    @staticmethod
    def rgb_to_integer(red, green, blue):
        """Convert RGB values to a 24-bit integer."""
        return (red << 16) | (green << 8) | blue

    @staticmethod
    def integer_to_rgb(color_integer):
        """Convert a 24-bit integer to RGB values."""
        red = (color_integer >> 16) & 0xFF
        green = (color_integer >> 8) & 0xFF
        blue = color_integer & 0xFF
        return red, green, blue
