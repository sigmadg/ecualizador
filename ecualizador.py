bl_info = {
    "name": "Ecualizador",
    "version": (1, 0),
    "blender": (2, 7, 1)
}

import bpy
import math

# Definimos la base para cálculos exponenciales
base = math.pow(2, (1. / 3))

def calcular(argumento_x):
    """
    Calcula el valor de la función tercia ignorando los límites establecidos.
    :param argumento_x: argumento x para la función
    :return: valor y calculado
    """
    return base ** argumento_x

def calcular_inverso(argumento_y):
    """
    Calcula el inverso de la función tercia.
    :param argumento_y: argumento y para la función
    :return: valor x correspondiente
    """
    if argumento_y <= 0:
        return 0
    return math.log(argumento_y, base)

def obtener_valor_desde_x(xx, minimo_x, maximo_x):
    """
    Calcula el valor desde el porcentaje en el intervalo.
    Ej: .42 significa 42%
    :param xx: Porcentaje en el intervalo. Debe estar en el rango [0,1]
    :param minimo_x: Límite inferior de x
    :param maximo_x: Límite superior de x
    :return: valor correspondiente de la función Tercia
    """
    assert (0 <= xx <= 1)
    return calcular(xx * (maximo_x - minimo_x) + minimo_x)

# Función para inicializar las propiedades en la escena de Blender
def iniciar_propiedades():
    # Propiedad para habilitar o deshabilitar la rotación del slash
    bpy.types.Scene.rotar_slash = bpy.props.BoolProperty(
        name="Rotación",
        description="Rotación de Slash",
        update=actualizar_slash)
    
    # Propiedad para definir la cantidad de slash
    bpy.types.Scene.slash = bpy.props.FloatProperty(
        name="Slash",
        default=0.0,
        description="Introduce un número flotante",
        update=actualizar_slash)   
            
    # Propiedad para habilitar o deshabilitar el zenit
    bpy.types.Scene.zenit = bpy.props.BoolProperty(
        name="Zenit",
        description="Zenit")
            
    # Propiedad para habilitar o deshabilitar la acumulación
    bpy.types.Scene.acumular = bpy.props.BoolProperty(
        name="Acumular",
        description="Acumular")

    # Propiedad para habilitar o deshabilitar el modo aditivo
    bpy.types.Scene.aditivo = bpy.props.BoolProperty(
        name="Usar aditivo",
        description="Usar aditivo")

    # Propiedad para habilitar o deshabilitar el modo cuadrado
    bpy.types.Scene.cuadrado = bpy.props.BoolProperty(
        name="Cuadrado",
        description="Cuadrado")

    # Propiedad para establecer el umbral del sonido
    bpy.types.Scene.umbral_sonido = bpy.props.FloatProperty(
        name="Umbral Sonido",
        default=0.1)    

    # Propiedad para establecer el umbral general
    bpy.types.Scene.umbral = bpy.props.FloatProperty(
        name="Umbral",
        default=0.0)    

    # Propiedad para establecer el tiempo de liberación
    bpy.types.Scene.liberar = bpy.props.FloatProperty(
        name="Liberar",
        default=0.2)    

    # Propiedad para establecer el tiempo de ataque
    bpy.types.Scene.ataque = bpy.props.FloatProperty(
        name="Ataque",
        default=0.005)    

    # Propiedades para la escala del cubo en los ejes X, Y y Z
    bpy.types.Scene.escala_cubo_x = bpy.props.FloatProperty(
        name="Escala X",
        default=1.0,
        min=0, 
        step=1,
        precision=2,
        description="Introduce un número flotante",
        update=actualizar_escala)    

    bpy.types.Scene.escala_cubo_y = bpy.props.FloatProperty(
        name="Escala Y",
        default=1.0,
        min=0, 
        step=1,
        precision=2,
        description="Introduce un número flotante",
        update=actualizar_escala)   

    bpy.types.Scene.escala_cubo_z = bpy.props.FloatProperty(
        name="Escala Z",
        default=5.6,
        min=0, 
        step=1,
        precision=2,
        description="Introduce un número flotante",
        update=actualizar_escala)       

    # Propiedad para seleccionar el tipo de visualización
    bpy.types.Scene.tipo_visualizacion = bpy.props.EnumProperty(
        items=[('0', 'Array', 'array'),
               ('1', 'Escalado de Objeto', 'object'),
               ('2', 'Escalado de Objeto Central', 'center_object')],
        name="Tipo de Visualización",
        update=actualizar_canales)      

    # Propiedad para habilitar o deshabilitar la depuración de frecuencia
    bpy.types.Scene.debug_frecuencia = bpy.props.BoolProperty(
        name="Depuración de Frecuencia",
        description="Introduce un valor booleano")

    # Propiedad para establecer la potencia del conductor
    bpy.types.Scene.potencia_conductor = bpy.props.FloatProperty(
        name="Potencia del Conductor",
        default=20.0,
        min=0, 
        step=5,
        precision=2,
        description="Introduce un número flotante",
        update=actualizar_conductores3)     
    
    # Propiedad para seleccionar el modo de frecuencia
    bpy.types.Scene.modo_frecuencia = bpy.props.EnumProperty(
        items=[('0', 'Logaritmo', 'log'),
               ('1', 'Lineal', 'linear'),
               ('2', 'Tercia (recomendado)', 'tercja')],
        name="Modo de Frecuencia")  
    
    # Propiedades para establecer las frecuencias mínima y máxima
    bpy.types.Scene.frecuencia_minima = bpy.props.FloatProperty(
        name="Frecuencia Mínima",
        default=100.0,
        min=0, 
        step=1000,
        precision=2,
        description="Introduce un número flotante")    
            
    bpy.types.Scene.frecuencia_maxima = bpy.props.FloatProperty(
        name="Frecuencia Máxima",
        default=20000.0,
        min=0, 
        step=1000,
        precision=2,
        description="Introduce un número flotante")        
    
    # Propiedad para establecer el espacio del array
    bpy.types.Scene.espacio_array = bpy.props.FloatProperty(
        name="Espacio de Array",
        default=1.5,
        min=0, 
        step=1,
        precision=2,
        description="Introduce un número flotante",
        update=actualizar_espacio_array)        
    
    # Propiedad para establecer el fotograma de inicio
    bpy.types.Scene.inicio = bpy.props.IntProperty(
        name="Fotograma de Inicio",
        default=1,
        min=1,
        description="Introduce un número entero")
    
    # Propiedades para definir las rutas de los archivos de los canales izquierdo y derecho
    bpy.types.Scene.archivo_izquierdo = bpy.props.StringProperty(
        name="Archivo Izquierdo",
        description="Define la ruta del archivo del canal izquierdo",
        subtype='FILE_PATH')

    bpy.types.Scene.archivo_derecho = bpy.props.StringProperty(
        name="Archivo Derecho",
        description="Define la ruta del archivo del canal derecho",
        subtype='FILE_PATH')    

    # Propiedades para la escala en los ejes X, Y y Z
    bpy.types.Scene.escala_x = bpy.props.FloatProperty(
        name="Escala X",
        default=0.7,
        min=0, 
        step=1,
        precision=2,
        description="Introduce un número flotante",
        update=actualizar_escala)    

    bpy.types.Scene.escala_y = bpy.props.FloatProperty(
        name="Escala Y",
        default=0.6,
        min=0, 
        step=1,
        precision=2,
        description="Introduce un número flotante",
        update=actualizar_escala)   

    bpy.types.Scene.escala_z = bpy.props.FloatProperty(
        name="Escala Z",
        default=0.4,
        min=0, 
        step=1,
        precision=2,
        description="Introduce un número flotante",
        update=actualizar_escala)                   
    
    # Propiedad para seleccionar los canales (Estéreo, Izquierdo, Derecho)
    bpy.types.Scene.canales = bpy.props.EnumProperty(
        items=[('0', 'Estéreo', 'Canal Izquierdo y Derecho'),
               ('1', 'Izquierdo', 'Canal Izquierdo'),
               ('2', 'Derecho', 'Canal Derecho')],
        name="Canales",
        update=actualizar_canales)
        
    # Propiedades para definir el espacio central y en el eje X
    bpy.types.Scene.espacio_central = bpy.props.FloatProperty(
        name="Espacio Central",
        default=2.0,
        min=0, 
        description="Introduce un número flotante",
        update=actualizar_espacio_x)    
    
    bpy.types.Scene.espacio_x = bpy.props.FloatProperty(
        name="Espacio X",
        default=2.0,
        min=0, 
        step=1,
        precision=2,
        description="Introduce un número flotante",
        update=actualizar_espacio_x)
    
    # Propiedad para establecer la cantidad de elementos en el eje X
    bpy.types.Scene.cantidad_x = bpy.props.IntProperty(
        name="Cantidad X",
        default=5,
        min=1,
        options={'ANIMATABLE'},
        description="Introduce un número entero",
        update=actualizar_cantidad)
    
# Función para iniciar los valores de las propiedades
def iniciar_valores_propiedades():
    bpy.context.scene['espacio_x'] = 0.2
    bpy.context.scene['cantidad_x'] = 32
    bpy.context.scene['espacio_central'] = 0.2
    bpy.context.scene['canales'] = 2
    bpy.context.scene['escala_x'] = 0.07
    bpy.context.scene['escala_y'] = 0.06
    bpy.context.scene['escala_z'] = 0.04
    bpy.context.scene['inicio'] = 100
    bpy.context.scene['espacio_array'] = 1.7
    bpy.context.scene['frecuencia_minima'] = 10.0
    bpy.context.scene['frecuencia_maxima'] = 20000.0  
    bpy.context.scene['modo_frecuencia'] = 2
    bpy.context.scene['potencia_conductor'] = 20.0
    bpy.context.scene['debug_frecuencia'] = False
    bpy.context.scene['tipo_visualizacion'] = 0    
    bpy.context.scene['escala_cubo_x'] = 0.07
    bpy.context.scene['escala_cubo_y'] = 0.06
    bpy.context.scene['escala_cubo_z'] = 0.20
    bpy.context.scene['zenit'] = False
    bpy.context.scene['slash'] = 0.0
    bpy.context.scene['rotar_slash'] = True
    
    bpy.context.scene['ataque'] = 0.005 
    bpy.context.scene['liberar'] = 0.2 
    bpy.context.scene['umbral'] = 0.0
    bpy.context.scene['acumular'] = False
    bpy.context.scene['aditivo'] = False
    bpy.context.scene['cuadrado'] = False
    bpy.context.scene['umbral_sonido'] = 0.1
    
    bpy.context.scene['iniciar'] = 1

calcular = 1

# Clase para crear un panel en el contexto de la escena del editor de propiedades
class AVPanel(bpy.types.Panel):
    """Crea un Panel en el contexto de la escena del editor de propiedades"""
    bl_label = "Visualización Audio Visual"
    bl_idname = "ESCENA_PT_layout"
    bl_space_type = 'PROPIEDADES'
    bl_region_type = 'VENTANA'
    bl_context = "escena"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.operator("object.crear_base_visualizador", icon="MODIFICADOR", text="(re)Crear Base del Visualizador")
        try:
            if bpy.context.scene['iniciar'] == 1:
                layout.label(text="Parámetros:", icon="UI")
                row = layout.row()
                row.prop(scene, "espacio_central") 
                row = layout.row(align=True)
                row.prop(scene, "cantidad_x")        
                row.prop(scene, "espacio_x")
                row = layout.row() 
                row.prop(scene, "slash")
                row.prop(scene, "rotar_slash", icon="ROTAR_MAN")  

                # Dependiendo del tipo de visualización, se muestran diferentes propiedades
                try:
                    if bpy.context.scene['tipo_visualizacion'] == 0:
                        row = layout.row()
                        row.prop(scene, "tipo_visualizacion", icon="MOD_ARRAY", text="Modo")                         
                        split = layout.split()
                        col = split.column()
                        col.label(text="Escala del Objeto:", icon="MANIPUL")
                        col = split.column(align=True)
                        col.prop(scene, 'escala_x', text="X")
                        col.prop(scene, 'escala_y', text="Y")
                        col.prop(scene, 'escala_z', text="Z")
                        row = layout.row()
                        row.label(text="Espacio del modificador Array:", icon="DESVINCULADO")
                        row.prop(scene, "espacio_array")
                    else:
                        row = layout.row()
                        row.prop(scene, "tipo_visualizacion", icon="MESH_CUBO", text="Modo")                             
                        split = layout.split()
                        col = split.column()
                        col.label(text="Escala del Objeto:", icon="MANIPUL")
                        col = split.column(align=True)
                        col.prop(scene, 'escala_cubo_x', text="X")
                        col.prop(scene, 'escala_cubo_y', text="Y")
                        #col.prop(scene, 'escala_cubo_z', text="Z")
                        col.label(text="") 
                        row = layout.row()
                        row.label(text="")                          
                except:
                    layout.label(text="Faltan variables, por favor informa del error")

                row = layout.row()
                row = layout.row()
                row.prop(scene, "potencia_conductor")        
                
                row = layout.row()
                box = layout.box()
                box.label("Canales a hornear y ruta de archivos de audio:", icon="SONIDO")
                if bpy.context.scene['canales'] == 0:
                    box.prop(scene, "canales", icon="FLECHA_IZQ_DER")
                elif bpy.context.scene['canales'] == 1:
                    box.prop(scene, "canales", icon="ATRÁS")
                elif bpy.context.scene['canales'] == 2:
                    box.prop(scene, "canales", icon="ADELANTE")
                box.prop(scene, "archivo_izquierdo")
                box.prop(scene, "archivo_derecho")     
                row = layout.row()    
                row.prop(scene, "modo_frecuencia", icon="CURVA_RND")
                row = layout.row()  
                row.prop(scene, "inicio")
                row = layout.row()        
                row.prop(scene, "frecuencia_minima")                       
                row.prop(scene, "frecuencia_maxima")      
                row = layout.row()
                row.operator("object.hornear", icon="RADIO", text="(re)Hornear datos de animación")    
                row = layout.row() 
                row.label(text="")

                box = layout.box()
                box.label(text="'Opciones de Hornear Sonido a F-Curvas':", icon="UI")
                split = box.split()
                col = split.column(align=True)    
                col.prop(scene, 'ataque')
                col.prop(scene, 'liberar')
                col = split.column(align=True)  
                col.prop(scene, 'umbral')
                col.prop(scene, 'umbral_sonido')
                split = box.split()
                col = split.column()
           
                col.prop(scene, 'acumular')
                col = split.column()
                col.prop(scene, 'aditivo')
                col = split.column()        
                col.prop(scene, 'cuadrado')
                row = layout.row()
                row.operator("object.iniciar_variables", icon="COLOR", text="Iniciar/Restablecer Variables")   
        except:
            False

# Función para iniciar la visualización de audio
def inicio_av():
    try: 
        bpy.context.scene['iniciar']
    except:
        iniciar_valores_propiedades()        
   
    bpy.ops.object.select_all(action="DESELECT")
    try:
        for i in range(bpy.context.scene['cantidad_x']):
            name = "barra_d_" + str(i+1)
            bpy.data.objects[name].select = True  
        bpy.ops.object.delete()    
    except:
        False
    try:
        for i in range(bpy.context.scene['cantidad_x']):  
            name = "barra_i_" + str(i+1)      
            bpy.data.objects[name].select = True          
        bpy.ops.object.delete()
    except:
        False
        
    for i in range(bpy.context.scene['cantidad_x']):
        generar_objetos(i)
        
    if bpy.context.scene['canales'] == 1 or bpy.context.scene['canales'] == 0:    
        bpy.context.scene.objects.active = bpy.data.objects["barra_i_" + str(bpy.context.scene['cantidad_x'])]
        bpy.ops.object.select_pattern(pattern="barra_i_" + str(bpy.context.scene['cantidad_x']))
    if bpy.context.scene['canales'] == 2 or bpy.context.scene['canales'] == 0:
        bpy.context.scene.objects.active = bpy.data.objects["barra_d_" + str(bpy.context.scene['cantidad_x'])]
        bpy.ops.object.select_pattern(pattern="barra_d_" + str(bpy.context.scene['cantidad_x']))   
            
    bpy.types.Scene.todos_objetos = bpy.context.scene['cantidad_x']
    actualizar_conductores()  
    actualizar_slash(True, True)
    actualizar_espacio_x(True, True)

# Función para hornear la animación de visualización de audio
def hornear_av():
    ### Calcular valores para tercia
    tercia_x_min = calcular_inverso(bpy.context.scene['frecuencia_minima'])
    tercia_x_max = calcular_inverso(bpy.context.scene['frecuencia_maxima'])
    tercia_paso = (1/bpy.context.scene['cantidad_x'])
    ###

    try:
        bpy.types.Scene.objetos_horneados
    except:
        bpy.types.Scene.objetos_horneados = 0
        
    bpy.ops.object.select_all(action="DESELECT")
    try:
        for i in range(bpy.types.Scene.objetos_horneados):
            name = "objeto_d_" + str(i+1)
            bpy.data.objects[name].select = True  
        bpy.ops.object.delete()    
    except:
        False
    try:
        for i in range(bpy.types.Scene.objetos_horneados):  
            name = "objeto_i_" + str(i+1)      
            bpy.data.objects[name].select = True          
        bpy.ops.object.delete()
    except:
        False 

    b = bpy.context.scene['frecuencia_minima']
    c = (bpy.context.scene['frecuencia_maxima']-bpy.context.scene['frecuencia_minima'])/bpy.context.scene['cantidad_x']
    
    bpy.context.window_manager.progress_begin(0, 100)
    bpy.context.window_manager.progress_update(0)
    for i in range(bpy.context.scene['cantidad_x']):
        if bpy.context.scene['modo_frecuencia'] == 2:
            a = b
            b = obtener_valor_desde_x((i+1)*tercia_paso, tercia_x_min, tercia_x_max)    
        elif bpy.context.scene['modo_frecuencia'] == 1:
            b = ((bpy.context.scene['frecuencia_maxima']-bpy.context.scene['frecuencia_minima'])-c*(bpy.context.scene['cantidad_x']-i-1)) + bpy.context.scene['frecuencia_minima']
            a = ((bpy.context.scene['frecuencia_maxima']-bpy.context.scene['frecuencia_minima'])-c*(bpy.context.scene['cantidad_x']-i)) + bpy.context.scene['frecuencia_minima']
        elif bpy.context.scene['modo_frecuencia'] == 0:
            b = ((1 - math.log(bpy.context.scene['cantidad_x']-i, bpy.context.scene['cantidad_x']+1)) * (bpy.context.scene['frecuencia_maxima']-bpy.context.scene['frecuencia_minima'])) + bpy.context.scene['frecuencia_minima']
            a = ((1 - math.log(bpy.context.scene['cantidad_x']-i+1, bpy.context.scene['cantidad_x']+1)) * (bpy.context.scene['frecuencia_maxima']-bpy.context.scene['frecuencia_minima'])) + bpy.context.scene['frecuencia_minima']

        print(str(i) + ": " + str(round(a, 1)) + " Hz - " + str(round(b, 1)) + " Hz")
        if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:
            bpy.context.scene.frame_current = bpy.context.scene['inicio']
            bpy.ops.object.add(location=(-(i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2), bpy.context.scene['slash'] * i, -2))
            name = "objeto_i_" + str(i+1)            
            bpy.context.active_object.name = name
            
            bpy.ops.anim.keyframe_insert_menu(type='Escalado')
            if calcular == 1:
                bpy.context.area.type = 'EDITOR_GRAFICO'
                try:
                    bpy.ops.graph.sound_bake(filepath=bpy.context.scene['archivo_izquierdo'],
                        low=a, high=b,
                        attack=bpy.context.scene['ataque'],
                        release=bpy.context.scene['liberar'],
                        threshold=bpy.context.scene['umbral'],
                        use_accumulate=bpy.context.scene['acumular'],
                        use_additive=bpy.context.scene['aditivo'],
                        use_square=bpy.context.scene['cuadrado'],
                        sthreshold=bpy.context.scene['umbral_sonido']) 
                except:
                    False
                bpy.context.area.type = 'PROPIEDADES'
            
            if bpy.context.scene['canales'] == 0:
                bpy.context.window_manager.progress_update((i+0.5)/bpy.context.scene['cantidad_x'])

            if bpy.context.scene['debug_frecuencia'] == 1:
                bpy.ops.object.add(location=(-(i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2), bpy.context.scene['slash'] * i, -4))
                name = (str(i) + ": " + str(round(a, 1)) + " Hz - " + str(round(b, 1)) + " Hz")
                bpy.context.active_object.name = name            
            
        if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
            bpy.context.scene.frame_current = bpy.context.scene['inicio']
            bpy.ops.object.add(location=(i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2, bpy.context.scene['slash'] * i, -2))
            name = "objeto_d_" + str(i+1)
            bpy.context.active_object.name = name
            
            bpy.ops.anim.keyframe_insert_menu(type='Escalado')
            if calcular == 1:
                bpy.context.area.type = 'EDITOR_GRAFICO'
                try:
                    bpy.ops.graph.sound_bake(filepath=bpy.context.scene['archivo_derecho'],
                        low=a, high=b,
                        attack=bpy.context.scene['ataque'],
                        release=bpy.context.scene['liberar'],
                        threshold=bpy.context.scene['umbral'],
                        use_accumulate=bpy.context.scene['acumular'],
                        use_additive=bpy.context.scene['aditivo'],
                        use_square=bpy.context.scene['cuadrado'],
                        sthreshold=bpy.context.scene['umbral_sonido']) 
                except:
                    False
                bpy.context.area.type = 'PROPIEDADES'

            if bpy.context.scene['canales'] == 0:
                bpy.context.window_manager.progress_update((i+1)/bpy.context.scene['cantidad_x'])

            if bpy.context.scene['debug_frecuencia'] == 1:
                bpy.ops.object.add(location=(i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2, bpy.context.scene['slash'] * i, -4))
                name = (str(i) + ": " + str(round(a, 1)) + " Hz - " + str(round(b, 1)) + " Hz")
                bpy.context.active_object.name = name

        if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 2:
            bpy.context.window_manager.progress_update((i+1)/bpy.context.scene['cantidad_x'])        

    bpy.context.window_manager.progress_end()
    bpy.types.Scene.objetos_horneados = bpy.context.scene['cantidad_x']    

# Clase para iniciar las variables en la escena de Blender
class IniciarVariables(bpy.types.Operator):
    bl_idname = "object.iniciar_variables"
    bl_label = "IniciarVariables"
    bl_options = {'REGISTRAR', 'DESHACER'}
    
    def execute(self, context):
        iniciar_valores_propiedades()
        return {'TERMINADO'}
    
# Clase para crear la base del visualizador en la escena de Blender
class CrearBaseVisualizador(bpy.types.Operator):
    bl_idname = "object.crear_base_visualizador"
    bl_label = "CrearBaseVisualizador"
    bl_options = {'REGISTRAR', 'DESHACER'}
    
    def execute(self, context):
        inicio_av()
        return {'TERMINADO'}
    
# Clase para hornear la visualización de audio en la escena de Blender
class Hornear(bpy.types.Operator):
    bl_idname = "object.hornear"
    bl_label = "Hornear"
    bl_options = {'REGISTRAR', 'DESHACER'}
    
    def execute(self, context):
        hornear_av()
        actualizar_conductores()
        return {'TERMINADO'}
    
# Función para actualizar el espacio del array
def actualizar_espacio_array(self, context):
    for i in range(bpy.context.scene['cantidad_x']):
        if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:        
            name = "barra_i_" + str(i+1)
            bpy.data.objects[name].modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['espacio_array']            
        if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
            name = "barra_d_" + str(i+1)
            bpy.data.objects[name].modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['espacio_array']

# Función para actualizar la rotación y posición del slash
def actualizar_slash(self, context):    
    for i in range(bpy.context.scene['cantidad_x']):
        if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:        
            name = "barra_i_" + str(i+1)
            bpy.data.objects[name].location[1] = bpy.context.scene['slash'] * i
            if bpy.context.scene['rotar_slash'] == True:
                bpy.data.objects[name].rotation_euler[2] = -math.asin(bpy.context.scene['slash']/math.sqrt(math.pow(bpy.context.scene['espacio_x'],2) + math.pow(bpy.context.scene['slash'],2)))
            else:
                bpy.data.objects[name].rotation_euler[2] = 0
        if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
            name = "barra_d_" + str(i+1)
            bpy.data.objects[name].location[1] = bpy.context.scene['slash'] * i
            if bpy.context.scene['rotar_slash'] == True:
                bpy.data.objects[name].rotation_euler[2] = math.asin(bpy.context.scene['slash']/math.sqrt(math.pow(bpy.context.scene['espacio_x'],2) + math.pow(bpy.context.scene['slash'],2)))  
            else:
                bpy.data.objects[name].rotation_euler[2] = 0      
    try:
        bpy.types.Scene.objetos_horneados
        for i in range(bpy.types.Scene.objetos_horneados):
            if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:        
                name = "objeto_i_" + str(i+1)
                bpy.data.objects[name].location[1] = bpy.context.scene['slash'] * i
            if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
                name = "objeto_d_" + str(i+1)
                bpy.data.objects[name].location[1] = bpy.context.scene['slash']  * i
    except:
        False                

# Función para aplicar conductores a los objetos
def aplicar_conductores(i):
    if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:         
        name = "barra_i_" + str(i+1)
        name2 = "objeto_i_" + str(i+1)
        try:
            bpy.data.objects[name2]
            if bpy.context.scene['tipo_visualizacion'] == 0:
                try:
                    bpy.data.objects[name].modifiers['Array'].driver_remove('count')
                except:
                    False   
                obj = bpy.data.objects[name] 
                mdf = obj.modifiers['Array'].driver_add('count')
                drv = mdf.driver
                drv.type = 'AVERAGE'
                var = drv.variables.new()
                var.name = 'name'
                var.type = 'TRANSFORMS'
                targ = var.targets[0]
                targ.id = bpy.data.objects[name2]
                targ.transform_type = 'SCALE_Z'
                targ.bone_target = 'Conductor'
                fmod = mdf.modifiers[0]
                fmod.poly_order = 1
                fmod.coefficients = (0.0, bpy.context.scene['potencia_conductor'])

            elif bpy.context.scene['tipo_visualizacion'] == 1 o bpy.context.scene['tipo_visualizacion'] == 2:
                try:
                    bpy.data.objects[name].driver_remove('scale', 2)
                except:
                    False   
                obj = bpy.data.objects[name] 
                mdf = obj.driver_add('scale', 2)
                drv = mdf.driver
                drv.type = 'AVERAGE'
                var = drv.variables.new()
                var.name = 'name'
                var.type = 'TRANSFORMS'
                targ = var.targets[0]
                targ.id = bpy.data.objects[name2]
                targ.transform_type = 'SCALE_Z'
                targ.bone_target = 'Conductor'
                fmod = mdf.modifiers[0]
                fmod.poly_order = 1
                fmod.coefficients = (0.0, bpy.context.scene['potencia_conductor'])
        except:
            False

    if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:            
        name = "barra_d_" + str(i+1)     
        name2 = "objeto_d_" + str(i+1)  
        try:
            bpy.data.objects[name2]
            if bpy.context.scene['tipo_visualizacion'] == 0:
                try:
                    bpy.data.objects[name].modifiers['Array'].driver_remove('count')
                except:
                    False    
                obj = bpy.data.objects[name] 
                mdf = obj.modifiers['Array'].driver_add('count')
                drv = mdf.driver
                drv.type = 'AVERAGE'
                var = drv.variables.new()
                var.name = 'name'
                var.type = 'TRANSFORMS'
                targ = var.targets[0]
                targ.id = bpy.data.objects[name2]
                targ.transform_type = 'SCALE_Z'
                targ.bone_target = 'Conductor'
                fmod = mdf.modifiers[0]
                fmod.poly_order = 1
                fmod.coefficients = (0.0, bpy.context.scene['potencia_conductor'])

            elif bpy.context.scene['tipo_visualizacion'] == 1 o bpy.context.scene['tipo_visualizacion'] == 2:
                try:
                    bpy.data.objects[name].driver_remove('scale', 2)
                except:
                    False    
                obj = bpy.data.objects[name] 
                mdf = obj.driver_add('scale', 2)
                drv = mdf.driver
                drv.type = 'AVERAGE'
                var = drv.variables.new()
                var.name = 'name'
                var.type = 'TRANSFORMS'
                targ = var.targets[0]
                targ.id = bpy.data.objects[name2]
                targ.transform_type = 'SCALE_Z'
                targ.bone_target = 'Conductor'
                fmod = mdf.modifiers[0]
                fmod.poly_order = 1
                fmod.coefficients = (0.0, bpy.context.scene['potencia_conductor'])
        except:
            False

# Función para actualizar conductores
def actualizar_conductores():
    try:
        bpy.types.Scene.objetos_horneados
        for i in range(bpy.types.Scene.objetos_horneados):
            aplicar_conductores(i)
    except:
        False

def actualizar_conductores3(self, context):
    try:
        bpy.types.Scene.objetos_horneados
        for i in range(bpy.types.Scene.objetos_horneados):
            aplicar_conductores(i)
    except:
        False
        
def actualizar_conductores2():
    try:
        bpy.types.Scene.objetos_horneados
        for i in range(bpy.types.Scene.todos_objetos, bpy.types.Scene.objetos_horneados):
            aplicar_conductores(i)
    except:
        False       

# Función para actualizar los canales
def actualizar_canales(self, context):
    inicio_av()

# Función para actualizar el espacio en el eje X
def actualizar_espacio_x(self, context):
    for i in range(bpy.context.scene['cantidad_x']):
        if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:        
            name = "barra_i_" + str(i+1)
            bpy.data.objects[name].location[0] = -(i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2)
            if bpy.context.scene['rotar_slash'] == True and (bpy.context.scene['espacio_x'] + bpy.context.scene['slash']) != 0:
                bpy.data.objects[name].rotation_euler[2] = -math.asin(bpy.context.scene['slash']/math.sqrt(math.pow(bpy.context.scene['espacio_x'],2) + math.pow(bpy.context.scene['slash'],2)))  
            else:
                bpy.data.objects[name].rotation_euler[2] = 0    
        if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
            name = "barra_d_" + str(i+1)
            bpy.data.objects[name].location[0] = i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2
            if bpy.context.scene['rotar_slash'] == True and (bpy.context.scene['espacio_x'] + bpy.context.scene['slash']) != 0:
                bpy.data.objects[name].rotation_euler[2] = math.asin(bpy.context.scene['slash']/math.sqrt(math.pow(bpy.context.scene['espacio_x'],2) + math.pow(bpy.context.scene['slash'],2)))  
            else:
                bpy.data.objects[name].rotation_euler[2] = 0                
    try:
        bpy.types.Scene.objetos_horneados
        for i in range(bpy.types.Scene.objetos_horneados):
            if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:        
                name = "objeto_i_" + str(i+1)
                bpy.data.objects[name].location[0] = -(i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2)
            if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
                name = "objeto_d_" + str(i+1)
                bpy.data.objects[name].location[0] = i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2            
    except:
        False

# Función para actualizar la escala de los objetos
def actualizar_escala(self, context):
    for i in range(bpy.context.scene['cantidad_x']):
        if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:        
            name = "barra_i_" + str(i+1)
            if bpy.context.scene['tipo_visualizacion'] == 0:
                bpy.data.objects[name].scale = (bpy.context.scene['escala_x'], bpy.context.scene['escala_y'], bpy.context.scene['escala_z'])
            elif bpy.context.scene['tipo_visualizacion'] == 1:
                bpy.data.objects[name].scale = (bpy.context.scene['escala_cubo_x'], bpy.context.scene['escala_cubo_y'], bpy.context.scene['escala_cubo_z'])
            elif bpy.context.scene['tipo_visualizacion'] == 2:
                bpy.data.objects[name].scale = (bpy.context.scene['escala_cubo_x'], bpy.context.scene['escala_cubo_y'], bpy.context.scene['escala_cubo_z']*2) 
        if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
            name = "barra_d_" + str(i+1)
            if bpy.context.scene['tipo_visualizacion'] == 0:
                bpy.data.objects[name].scale = (bpy.context.scene['escala_x'], bpy.context.scene['escala_y'], bpy.context.scene['escala_z'])
            elif bpy.context.scene['tipo_visualizacion'] == 1:
                bpy.data.objects[name].scale = (bpy.context.scene['escala_cubo_x'], bpy.context.scene['escala_cubo_y'], bpy.context.scene['escala_cubo_z'])
            elif bpy.context.scene['tipo_visualizacion'] == 2:
                bpy.data.objects[name].scale = (bpy.context.scene['escala_cubo_x'], bpy.context.scene['escala_cubo_y'], bpy.context.scene['escala_cubo_z']*2) 

# Función para generar los objetos en la escena
def generar_objetos(i):
    guardar_posicion = bpy.context.scene.cursor_location.copy()
    if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:
        bpy.ops.mesh.primitive_cube_add(location=(-(i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2), bpy.context.scene['slash'] * i, 0))
        if bpy.context.scene['rotar_slash'] == True:
            bpy.context.active_object.rotation_euler[2] = -math.asin(bpy.context.scene['slash']/math.sqrt(math.pow(bpy.context.scene['espacio_x'],2) + math.pow(bpy.context.scene['slash'],2)))  
            
        if bpy.context.scene['tipo_visualizacion'] == 0:
            bpy.context.active_object.scale = (bpy.context.scene['escala_x'], bpy.context.scene['escala_y'], bpy.context.scene['escala_z'])
        elif bpy.context.scene['tipo_visualizacion'] == 1:
            bpy.context.active_object.scale = (1, 1, 0.06)
            bpy.ops.object.transform_apply(scale=True)
            bpy.context.active_object.location[2] = 0.06
            bpy.context.scene.cursor_location = (-(i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2), bpy.context.scene['slash'] * i, 0)  
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR') 
            bpy.context.active_object.scale = (bpy.context.scene['escala_cubo_x'], bpy.context.scene['escala_cubo_y'], bpy.context.scene['escala_cubo_z'])
        elif bpy.context.scene['tipo_visualizacion'] == 2:
            bpy.context.active_object.scale = (1, 1, 0.06*2)
            bpy.ops.object.transform_apply(scale=True)
            bpy.context.active_object.scale = (bpy.context.scene['escala_cubo_x'], bpy.context.scene['escala_cubo_y'], bpy.context.scene['escala_cubo_z']*2)
                
        name = "barra_i_" + str(i+1)
        bpy.context.active_object.name = name

        if bpy.context.scene['tipo_visualizacion'] == 0:
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.active_object.modifiers['Array'].count = 10                
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['espacio_array']
                
    if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
        bpy.ops.mesh.primitive_cube_add(location=(i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2, bpy.context.scene['slash'] * i, 0))
        if bpy.context.scene['rotar_slash'] == True:
            bpy.context.active_object.rotation_euler[2] = math.asin(bpy.context.scene['slash']/math.sqrt(math.pow(bpy.context.scene['espacio_x'],2) + math.pow(bpy.context.scene['slash'],2)))  
            
        if bpy.context.scene['tipo_visualizacion'] == 0:
            bpy.context.active_object.scale = (bpy.context.scene['escala_x'], bpy.context.scene['escala_y'], bpy.context.scene['escala_z'])
        elif bpy.context.scene['tipo_visualizacion'] == 1:
            bpy.context.active_object.scale = (1, 1, 0.06)
            bpy.ops.object.transform_apply(scale=True)
            bpy.context.active_object.location[2] = 0.06
            bpy.context.scene.cursor_location = (i*bpy.context.scene['espacio_x'] + bpy.context.scene['espacio_central']/2, bpy.context.scene['slash'] * i, 0)
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')      
            bpy.context.active_object.scale = (bpy.context.scene['escala_cubo_x'], bpy.context.scene['escala_cubo_y'], bpy.context.scene['escala_cubo_z'])       
        elif bpy.context.scene['tipo_visualizacion'] == 2:
            bpy.context.active_object.scale = (1, 1, 0.06*2)
            bpy.ops.object.transform_apply(scale=True)
            bpy.context.active_object.scale = (bpy.context.scene['escala_cubo_x'], bpy.context.scene['escala_cubo_y'], bpy.context.scene['escala_cubo_z']*2)

        name = "barra_d_" + str(i+1)
        bpy.context.active_object.name = name
               
        if bpy.context.scene['tipo_visualizacion'] == 0:
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.active_object.modifiers['Array'].count = 10                     
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['espacio_array']
    bpy.context.scene.cursor_location = guardar_posicion  
        
# Función para actualizar la cantidad de elementos en el eje X
def actualizar_cantidad(self, context):
    if bpy.types.Scene.todos_objetos > bpy.context.scene['cantidad_x']:
        bpy.ops.object.select_all(action="DESELECT")
        for i in range(bpy.context.scene['cantidad_x'], bpy.types.Scene.todos_objetos):
            if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:            
                name = "barra_i_" + str(i+1)
                bpy.data.objects[name].select = True     
            if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
                name = "barra_d_" + str(i+1)
                bpy.data.objects[name].select = True
        bpy.ops.object.delete()
        
        if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:    
            bpy.context.scene.objects.active = bpy.data.objects["barra_i_" + str(bpy.context.scene['cantidad_x'])]
            bpy.ops.object.select_pattern(pattern="barra_i_" + str(bpy.context.scene['cantidad_x'])]
        if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
            bpy.context.scene.objects.active = bpy.data.objects["barra_d_" + str(bpy.context.scene['cantidad_x'])]
            bpy.ops.object.select_pattern(pattern="barra_d_" + str(bpy.context.scene['cantidad_x'])])            
            
        bpy.types.Scene.todos_objetos = bpy.context.scene['cantidad_x']
    elif bpy.types.Scene.todos_objetos < bpy.context.scene['cantidad_x']:
        for i in range(bpy.types.Scene.todos_objetos, bpy.context.scene['cantidad_x']):
            generar_objetos(i)
            try:
                if bpy.types.Scene.todos_objetos < bpy.types.Scene.objetos_horneados:
                    actualizar_conductores2()
            except:
                False
     
        if bpy.context.scene['canales'] == 1 o bpy.context.scene['canales'] == 0:    
            bpy.context.scene.objects.active = bpy.data.objects["barra_i_" + str(bpy.context.scene['cantidad_x'])]
            bpy.ops.object.select_pattern(pattern="barra_i_" + str(bpy.context.scene['cantidad_x'])]
        if bpy.context.scene['canales'] == 2 o bpy.context.scene['canales'] == 0:
            bpy.context.scene.objects.active = bpy.data.objects["barra_d_" + str(bpy.context.scene['cantidad_x'])]
            bpy.ops.object.select_pattern(pattern="barra_d_" + str(bpy.context.scene['cantidad_x'])]
        bpy.types.Scene.todos_objetos = bpy.context.scene['cantidad_x']
    else:
        False

# Función para registrar las clases y propiedades en Blender
def registrar():
    bpy.utils.register_class(CrearBaseVisualizador)
    bpy.utils.register_class(IniciarVariables)
    bpy.utils.register_class(Hornear)    
    bpy.utils.register_class(AVPanel)
    iniciar_propiedades()

# Función para desregistrar las clases y propiedades en Blender
def desregistrar():
    bpy.utils.unregister_class(CrearBaseVisualizador)
    bpy.utils.unregister_class(IniciarVariables)
    bpy.utils.unregister_class(Hornear)    
    bpy.utils.unregister_class(AVPanel)

if __name__ == "__main__":
    registrar()
