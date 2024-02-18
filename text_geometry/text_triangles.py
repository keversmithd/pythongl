import freetype
import os
from scipy.spatial import Delaunay

class TextGeometry:

    char_ranges = [[33,126]]

    triangulated_text = []
    chars_loaded = 0
    charmap = {}

    def LoadActiveFont(self,filepath):

        if(len(self.triangulated_text) > 0):
            self.triangulated_text.clear()
            chars_loaded = 0

        current_directory = os.getcwd()
        filepath = current_directory + "\\" + filepath
        face = freetype.Face(filepath)

        for i in range(len(self.char_ranges)):
            for j in range(len(self.char_ranges[i])):
                face.load_glyph(self.char_ranges[i][0]+j, freetype.FT_LOAD_NO_BITMAP)
                outline = face.glyph.outline

                width = face.bbox.xMax - face.bbox.xMin
                height = face.bbox.yMax - face.bbox.yMin
                
                aspect_ratio = height/width

                scale_between = aspect_ratio

                #then width is scaled between 1
                #and height is scaled between scale_between

                outline_points = outline.points
                # Assuming you have the glyph outline points

                triangles = Delaunay(outline_points)
                self.triangulated_text.append([triangles.points,triangles.simplices])
                self.charmap[self.char_ranges[i][0]+j] = [self.chars_loaded, face.glyph.advance.x]
                self.chars_loaded += 1

        
                

joanRegular = TextGeometry()
joanRegular.LoadActiveFont("fonts\\Joan-Regular.ttf")



                

        

