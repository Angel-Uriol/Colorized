import struct


# Class to represent a pixel
class Pixel:
    def __init__(self, r=0, g=0, b=0):
        self.red = r
        self.green = g
        self.blue = b

# Class to represent a BMP image
class BMPImage:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.pixels = []  # List to store pixel data

    # Function to load BMP image from file
    def load_image(self, filename):
        try:
            with open(filename, "rb") as file:
                header = file.read(54)
                self.width = struct.unpack('<i', header[18:22])[0]
                self.height = struct.unpack('<i', header[22:26])[0]
                if struct.unpack('<i', header[28:32])[0] != 24 or struct.unpack('<i', header[30:34])[0] != 0:
                    print("Error: Unsupported BMP format. Only 24-bit BMP without compression is supported.")
                    return False

                self.pixels.clear()
                padding = (4 - (self.width * 3) % 4) % 4
                for _ in range(self.height):
                    row = []
                    for _ in range(self.width):
                        blue, green, red = struct.unpack('BBB', file.read(3))
                        row.append(Pixel(red, green, blue))
                    file.read(padding)
                    self.pixels.append(row)
            return True
        except FileNotFoundError:
            print("Error: Could not open BMP file", filename)
            return False

    # Function to get the width of the image
    def get_width(self):
        return self.width

    # Function to get the height of the image
    def get_height(self):
        return self.height

    # Function to get the pixels of the image
    def get_pixels(self):
        return self.pixels

    # Function to calculate the average color of the pixels
    def calculate_average_color(self):
        sum_r, sum_g, sum_b = 0, 0, 0
        for row in self.pixels:
            for pixel in row:
                sum_r += pixel.red
                sum_g += pixel.green
                sum_b += pixel.blue
        pixel_count = self.width * self.height
        avg_r = sum_r // pixel_count
        avg_g = sum_g // pixel_count
        avg_b = sum_b // pixel_count
        return Pixel(avg_r, avg_g, avg_b)

    # Function to calculate the average color of a specific vertical part of the image
    def calculate_average_color_of_vertical_part(self, start_x, end_x):
        sum_r, sum_g, sum_b = 0, 0, 0
        pixel_count = 0
        for row in self.pixels:
            for x in range(start_x, end_x + 1):
                pixel = row[x]
                sum_r += pixel.red
                sum_g += pixel.green
                sum_b += pixel.blue
                pixel_count += 1
        avg_r = sum_r // pixel_count
        avg_g = sum_g // pixel_count
        avg_b = sum_b // pixel_count
        return Pixel(avg_r, avg_g, avg_b)

    # Function to calculate the average color of a specific horizontal part of the image
    def calculate_average_color_of_horizontal_part(self, start_y, end_y):
        sum_r, sum_g, sum_b = 0, 0, 0
        pixel_count = 0
        for y in range(start_y, end_y + 1):
            for pixel in self.pixels[y]:
                sum_r += pixel.red
                sum_g += pixel.green
                sum_b += pixel.blue
                pixel_count += 1
        avg_r = sum_r // pixel_count
        avg_g = sum_g // pixel_count
        avg_b = sum_b // pixel_count
        return Pixel(avg_r, avg_g, avg_b)

    # Function to calculate the average colors of the pixels in the top horizontal line
    def calculate_average_colors_of_top_horizontal_line(self, num_sections):
        avg_colors = []
        if num_sections <= 0:
            print("Error: Number of sections must be greater than zero.")
            return avg_colors

        step_size = self.width // num_sections

        for i in range(num_sections):
            start_x = i * step_size
            end_x = (i + 1) * step_size - 1

            sum_r, sum_g, sum_b = 0, 0, 0
            pixel_count = 0

            for x in range(start_x, end_x + 1):
                pixel = self.pixels[0][x]
                sum_r += pixel.red
                sum_g += pixel.green
                sum_b += pixel.blue
                pixel_count += 1

            avg_r = sum_r // pixel_count
            avg_g = sum_g // pixel_count
            avg_b = sum_b // pixel_count
            avg_colors.append(Pixel(avg_r, avg_g, avg_b))

        return avg_colors

    # Function to calculate the average colors of the pixels in the right vertical line
    def calculate_average_colors_of_right_vertical_line(self, num_sections):
        avg_colors = []
        if num_sections <= 0:
            print("Error: Number of sections must be greater than zero.")
            return avg_colors

        step_size = self.height // num_sections

        for i in range(num_sections):
            start_y = i * step_size
            end_y = (i + 1) * step_size - 1

            sum_r, sum_g, sum_b = 0, 0, 0
            pixel_count = 0

            for y in range(start_y, end_y + 1):
                pixel = self.pixels[y][-1]
                sum_r += pixel.red
                sum_g += pixel.green
                sum_b += pixel.blue
                pixel_count += 1

            avg_r = sum_r // pixel_count
            avg_g = sum_g // pixel_count
            avg_b = sum_b // pixel_count
            avg_colors.append(Pixel(avg_r, avg_g, avg_b))

        return avg_colors

    # Function to calculate the average colors of the pixels in the bottom horizontal line
    def calculate_average_colors_of_bottom_horizontal_line(self, num_sections):
        avg_colors = []
        if num_sections <= 0:
            print("Error: Number of sections must be greater than zero.")
            return avg_colors

        step_size = self.width // num_sections

        for i in range(num_sections):
            start_x = i * step_size
            end_x = (i + 1) * step_size - 1

            sum_r, sum_g, sum_b = 0, 0, 0
            pixel_count = 0

            for x in range(start_x, end_x + 1):
                pixel = self.pixels[-1][x]
                sum_r += pixel.red
                sum_g += pixel.green
                sum_b += pixel.blue
                pixel_count += 1

            avg_r = sum_r // pixel_count
            avg_g = sum_g // pixel_count
            avg_b = sum_b // pixel_count
            avg_colors.append(Pixel(avg_r, avg_g, avg_b))

        return avg_colors

    # Function to calculate the average colors of the pixels in the left vertical line
    def calculate_average_colors_of_vertical_part_with_subsections(self, start_x, end_x, num_subsections):
        avg_colors = []
        if num_subsections <= 0:
            print("Error: Number of subsections must be greater than zero.")
            return avg_colors

        start_x = max(0, min(start_x, self.width - 1))
        end_x = max(0, min(end_x, self.width - 1))

        range_width = end_x - start_x + 1
        subsection_width = range_width // num_subsections

        for i in range(num_subsections):
            subsection_start_x = start_x + i * subsection_width
            subsection_end_x = subsection_start_x + subsection_width - 1
            subsection_start_x = max(start_x, min(subsection_start_x, end_x))
            subsection_end_x = max(start_x, min(subsection_end_x, end_x))

            avg_color = self.calculate_average_color_of_vertical_part(subsection_start_x, subsection_end_x)
            avg_colors.append(avg_color)

        return avg_colors

# Example usage
bmp_image = BMPImage()
if not bmp_image.load_image("Raw_Blue.bmp"):
    exit(1)

print("Image Width:", bmp_image.get_width())
print("Image Height:", bmp_image.get_height())

pixels = bmp_image.get_pixels()
print("Number of pixels:", len(pixels))

avg_color = bmp_image.calculate_average_color()
print("Average Color: R={}, G={}, B={}".format(avg_color.red, avg_color.green, avg_color.blue))

vertical_divisions = 3
third_width = bmp_image.get_width() // vertical_divisions
for i in range(vertical_divisions):
    start_x = i * third_width
    end_x = (i + 1) * third_width - 1
    avg_color_vertical_part = bmp_image.calculate_average_color_of_vertical_part(start_x, end_x)
    print("Average Color of Vertical Part {}: R={}, G={}, B={}".format(i + 1, avg_color_vertical_part.red,
                                                                       avg_color_vertical_part.green,
                                                                       avg_color_vertical_part.blue))

horizontal_divisions = 3
third_height = bmp_image.get_height() // horizontal_divisions
avg_colors = []
for i in range(horizontal_divisions):
    start_y = i * third_height
    end_y = (i + 1) * third_height - 1
    avg_color_horizontal_part = bmp_image.calculate_average_color_of_horizontal_part(start_y, end_y)
    avg_colors.append(avg_color_horizontal_part)
    print("Average color of Horizontal Part {}: R={}, G={}, B={}".format(i + 1, avg_color_horizontal_part.red,
                                                                         avg_color_horizontal_part.green,
                                                                         avg_color_horizontal_part.blue))

num_sections = 12
top_horizontal_line = bmp_image.calculate_average_colors_of_top_horizontal_line(num_sections)
print("Top Horizontal Line:")
for pixel in top_horizontal_line:
    print("R={}, G={}, B={}".format(pixel.red, pixel.green, pixel.blue))

right_vertical_line = bmp_image.calculate_average_colors_of_right_vertical_line(num_sections)
print("Right Vertical Line:")
for pixel in right_vertical_line:
    print("R={}, G={}, B={}".format(pixel.red, pixel.green, pixel.blue))

bottom_horizontal_line = bmp_image.calculate_average_colors_of_bottom_horizontal_line(num_sections)
print("Bottom Horizontal Line:")
for pixel in bottom_horizontal_line:
    print("R={}, G={}, B={}".format(pixel.red, pixel.green, pixel.blue))

start_x = 28
precision = bmp_image.get_width() // 10
end_x = precision
left_vertical_line = bmp_image.calculate_average_colors_of_vertical_part_with_subsections(start_x, end_x, num_sections)
print("Left Vertical Line:")
for pixel in left_vertical_line:
    print("R={}, G={}, B={}".format(pixel.red, pixel.green, pixel.blue))
