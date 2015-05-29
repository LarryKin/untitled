# -*- coding: utf-8 -*-
"""
Created on Fri May 22 20:42:19 2015

@author: larry
"""

import os, pygame, glob 
from operator import itemgetter

class sprite_packer(): 
    
    def init(self, **kwargs):
    #defaults for input/output folders and texture size
        self.folder = kwargs.get("folder", "input") 
        self.outfolder = kwargs.get("outfolder", "output") 
        self.texturew = kwargs.get("texturew", 1024) 
        self.textureh = kwargs.get("textureh", 1024) 
    def Pack(self): 
        patterns = [".gif", ".png", "*.bmp"]
    
        #check for files in folder
        print os.path.abspath(self.folder) 
        result = [] 
        for pattern in patterns: 
            pattern = os.path.join(self.folder, pattern) 
            result.extend(glob.glob(pattern))
    
        if len(result) == 0: print "No files in input folder!" return
    
        #build a new texture
        print "processing %d files:" % len(result)
    
        texture = pygame.Surface((self.texturew, self.textureh), pygame.SRCALPHA, 32) 
        NodeTree = Node(texture, 0, 0, self.texturew, self.textureh)
    
        #sort our sprites by size
        sprites = [] 
        for filepath in result: 
            head, tail = os.path.split(filepath) 
            filename = tail 
            spritename, ext = os.path.splitext(tail) 
            surface = pygame.image.load(filepath) 
            #area should work as a proxy for size unless we get some badly 
            #out of proportion sprites 
            x,y = surface.get_rect().size size = x*y 
            sprites.append([filepath, spritename, size])
    
        sprites.sort(key = itemgetter(2), reverse=True) 
        print sprites 
        for filepath, spritename, size in sprites: 
            surface = pygame.image.load(filepath) 
            print "Inserting %s - %s" %(spritename, surface) 
            NodeTree.Insert(surface, spritename)
    
        #save the finished texture to outfolder
        outfile = os.path.join(self.outfolder, "texture.png") 
        mapfile = os.path.join(self.outfolder, "texmap.py") 
        pygame.image.save(texture, outfile) 
        print "texture written to %s" % outfile
    
        #now dump the list of nodes
        map = NodeTree.Dump(True) + "}" with open(mapfile, 'w') as f: f.write(map) 
        print "texture map written to %s" %mapfile 
        class Node(): 
            def init(self, texture, x, y, w, h): 
                print "Creating node %d, %d, %d, %d" %(x,y,w,h) 
                self.texture = texture self.bottom = None 
                self.right = None self.rect = [x,y,w,h] 
                self.imagerect = [0,0,0,0] 
                self.image = None 
            def Insert(self, surface, name): 
                if self.image != None: 
                    print "node at %s contains %s. Adding to child node" % (self.rect, self.image) 
                result = self.AddChild(surface, name) 
                if not result: 
                    print "Could not add %s!" %name 
                    return result
    
                x,y,myw,myh = self.rect 
                rect = surface.get_rect() 
                print "image size : (%d,%d)" % rect.size w,h = rect.size
    
                #add some padding around sprites
                h += 1 
                w += 1 
                if w > myw or h > myh: 
                    print "Node too small!" 
                    return False 
                print "adding to node at %s" % self.rect 
                self.texture.blit(surface, (x,y)) 
                self.image = name 
                self.imagerect = [x,y,w-1,h-1] 
                print self.imagerect
    
                #generate ChildNodes
                dw = myw - w 
                dh = myh - h 
                if dw > dh: 
                    self.right = Node(self.texture, x+w, y, dw, myh) 
                    self.bottom = Node(self.texture, x, y+h, w, dh) 
                else: 
                    self.right = Node(self.texture, x+w, y, dw, h) 
                    self.bottom = Node(self.texture, x, y+h, myw, dh) 
                return True
    
                def AddChild(self, surface, name): 
                    if not self.right.Insert(surface, name): 
                        return self.bottom.Insert(surface, name) 
                    return True
    '''
    dump structure
    {"filename" : [x,y,w,h],
    }
    '''
    def Dump(self, first = False):
    
        print "Dumping node"
        if self.image == None: 
            return ""
    
        result = "'%s' : %s,\n" % (self.image, self.imagerect) 
        if first: 
            result = "texmap = {\n%s" %result 
            result += self.right.Dump() result += self.bottom.Dump() 
            return result 
        packer = SpritePacker() 
        packer.Pack()
    
    
    

