from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PIC_SIZE = (80,40)
FONT_SIZE = 32
FONT_TYPE = 'arial.ttf'


class CodePic():

    def generate_picture(self):
        raise NotImplementedError

    @property
    def character(self):
        raise NotImplementedError

    @character.setter
    def character(self, value):
        raise NotImplementedError


class CodePicIntervene(CodePic):

    def __init__(self, element):
        self.element = element

    @property
    def character(self):
        return self.element.character

    @character.setter
    def character(self, value):
        self.element.character = value


class CodeBody(CodePic):

    def __init__(self, character):
        self._character = character

    @property
    def character(self):
        return self._character

    @character.setter
    def character(self, value):
        self._character = value

    def generate_picture(self):
        codePic = Image.new('RGBA', PIC_SIZE, 'white')
        draw = ImageDraw.Draw(codePic)
        font = ImageFont.truetype(FONT_TYPE, size=FONT_SIZE)
        draw.text((0, 0), self.character, fill='black', font=font)

        return codePic


class PointIntervene(CodePicIntervene):

    def generate_picture(self):
        import random
        codePic = self.element.generate_picture()
        x_size, y_size = codePic.size
        for x in range(x_size):
            for y in range(y_size):
                if random.randint(1, 9) % 2 == 0:
                    codePic.putpixel((x, y), (255, 255, 255, 0))
        return codePic


def makeAuthCode(character):
    f = BytesIO()
    cb = CodeBody(character)
    authcode = PointIntervene(cb)
    im = authcode.generate_picture()
    # im.show()
    im.save(f,'JPEG')
    return f.getvalue()

if __name__ == '__main__':
    makeAuthCode('fuck')
