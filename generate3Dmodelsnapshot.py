from pyexiv2 import Image
import os, math
import bpy

##########
# 1. Modify your IMAGE_FOLDER_PATH
# 2. Create Cube and position inside the middle of your 3d model roof
# 3. Name your created cube "RoofCenter"
# 4. Select route in view 
# 5. Run script

IMAGE_FOLDER_PATH = 'C:\\Users\\sebas\\Downloads\\Visuelle_Challenge_VISUAL\\Set_1_Airteam\\Aerial_photos_1\\'
RENDER_FOLDER_PATH = IMAGE_FOLDER_PATH + 'rendered'


def create_render_folder():
    if not os.path.exists(RENDER_FOLDER_PATH):
        os.mkdir(RENDER_FOLDER_PATH)


def get_metadata_from_image(image_path, filename):
    image = Image(image_path)
    
    xmp_metadata = image.read_xmp() # returns all metadata (EXIF, IPTC, XMP)
    print(image_path)
    gimbal_roll_degree = xmp_metadata['Xmp.drone-dji.GimbalRollDegree']
    gimbal_yaw_degree  = xmp_metadata['Xmp.drone-dji.GimbalYawDegree']
    gimbal_pitch_degree  = xmp_metadata['Xmp.drone-dji.GimbalPitchDegree']
    
    flight_roll_degree = xmp_metadata['Xmp.drone-dji.FlightRollDegree']
    flight_yaw_degree = xmp_metadata['Xmp.drone-dji.FlightYawDegree']
    flight_pitch_degree = xmp_metadata['Xmp.drone-dji.FlightPitchDegree']
    
    gimbal_roll_degree = gimbal_roll_degree.replace('+','')
    gimbal_yaw_degree = gimbal_yaw_degree.replace('+','')
    gimbal_pitch_degree = gimbal_pitch_degree.replace('+','')
    return {'name': filename,'roll': gimbal_roll_degree, 'yaw': gimbal_yaw_degree, 'pitch': gimbal_pitch_degree}
        
    
def load_images():
    image_data = []
    for filename in os.listdir(IMAGE_FOLDER_PATH):
        if not os.path.isdir(IMAGE_FOLDER_PATH + filename):
            image_data.append(get_metadata_from_image(IMAGE_FOLDER_PATH + filename, filename))
    return image_data


def calulate_center_polygons(image_data):
    ob = bpy.context.object
    me = ob.data

    for index, p in enumerate(me.polygons):
        p_center = [0.0, 0.0, 0.0]
        for v in p.vertices:
            p_center[0] += me.vertices[v].co[0]        
            p_center[1] += me.vertices[v].co[1]
            p_center[2] += me.vertices[v].co[2]
        p_center[0] /= len(p.vertices) # division by zero               
        p_center[1] /= len(p.vertices) # division by zero               
        p_center[2] /= len(p.vertices) # division by zero        
    
        image_data[index]['position'] = p_center
    return image_data


def get_roof_center_location():
    roof_center = bpy.data.objects['RoofCenter']
    return roof_center.location
    
    
def set_camera_rotation(obj_camera, point):
    loc_camera = obj_camera.location
    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()
    

def create_cameras_for_points(point_data):
    for point in point_data:
        camera_data = bpy.data.cameras.new(name='Camera_' + point['name'])
        camera_object = bpy.data.objects.new('Camera', camera_data)
        camera_object.location = point['position']
    
         
        camera_object.data.lens_unit = 'FOV'
        camera_object.data.angle = 1.14319
        
        roof_location = get_roof_center_location()
        set_camera_rotation(camera_object, roof_location)
        
        
        bpy.context.scene.collection.objects.link(camera_object)
        
        
def render_for_every_camera():
    for obj in bpy.data.objects:
        if obj.type != "CAMERA":
            continue
        scene = bpy.context.scene
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = IMAGE_FOLDER_PATH + obj.name + ".png"
        bpy.context.scene.camera = obj
        bpy.ops.render.render(write_still = 1)
        
        
def render_for_single_camera(camera_name, step, image_name_suffix):
        camera = bpy.data.objects[camera_name]
        scene = bpy.context.scene
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = RENDER_FOLDER_PATH + "_single_" + image_name_suffix + "_" + str(step) + ".png"
        bpy.context.scene.camera = camera
        bpy.ops.render.render(write_still = 1)
        
    
def change_height_of_camera(camera_object, steps, step_size):
        camera_object.location.z = camera_object.location.z + steps * step_size
        print(camera_object.location)
        roof_location = get_roof_center_location()
        set_camera_rotation(camera_object, roof_location)
        
        
def change_position_of_camera(camera_object, steps, step_size):
        camera_object.location.x = camera_object.location.x + steps * step_size
        camera_object.location.y = camera_object.location.y + steps * step_size
        roof_location = get_roof_center_location()
        set_camera_rotation(camera_object, roof_location)
    
    
# For creating more test images for matching
def create_more_images_for_camera():
        steps = 20
        step_size = 0.05
        camera_name = 'Camera.053'
        camera_object = bpy.data.objects[camera_name]
        original_camera_position_z = camera_object.location.z

        for y in range(0,steps):
            change_height_of_camera(camera_object, y, step_size)
            render_for_single_camera(camera_name, str(y * -1), "up")
            
        camera_object.location.z = original_camera_position_z
        
        for y in range(0,steps):
            change_height_of_camera(camera_object, y * -1, step_size)
            render_for_single_camera(camera_name, str(y * -1), "down")
    

create_render_folder()
bpy.context.scene.render.resolution_x = 5472
bpy.context.scene.render.resolution_y = 3648

image_data = load_images()
point_data = calulate_center_polygons(image_data)
create_cameras_for_points(point_data)
render_for_every_camera()




