from PIL import Image,ImageDraw,ImageFont
import random
"""
该模块用于生成验证码。
用法示例：
1、实例化一个具体对象
    code_identify = CheckCode(70,30,25)
2、调用picture_generator()生成一个具体的验证码图片，赶回图片对象和字符串对象
    img,code = code_identify.picture_generator()
"""


class CheckCode(object):
    """
    验证码类，初始化参数：
    图片宽：width默认120px
    图片高：height默认40px
    图片中字体大小：font_size默认36
    """
    def __init__(self,width = 120,height = 40,font_size = 36):
        # 初始化图片的长宽和字体大小
        self.width = width
        self.height = height
        self.font_size = font_size

    @staticmethod
    def content_generator():
        """
        :return: 从source中选择的4个随机字符串
        """
        source = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                  'H', 'I', 'J', 'K','L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        content_list = random.sample(source,4)
        return "".join(content_list)

    def picture_generator(self):
        """
        :return: 返回图片对象以及图片上的字符串组成的元组
        """
        # 生成图片对象
        image = Image.new("RGB",(self.width,self.height),(255,255,255))
        # 生成字体对象，需要两个参数，一个字体文件，一个字体大小
        font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', self.font_size)
        # 生成一个画笔对象
        draw = ImageDraw.Draw(image)
        # 产生字符串
        content = self.content_generator()
        # 将产生的字符串画在图片对象上
        draw.text((self.width*0,self.height*0.15),content,fill=(30,0,0),font=font)
        # 画上干扰线
        begin = (0, random.randint(0, self.height))
        end = (self.width, random.randint(0, self.height))
        draw.line([begin, end], fill=(0, 0, 0), width=3)
        return image,content