from djitellopy import Tello  # Importa la biblioteca para controlar el drone DJI Tello
import cv2  # Importa OpenCV para el manejo de imágenes y video

frame_source = 1  # Variable para determinar la fuente del video (1 indica uso del drone)

if (frame_source == 1):
    drone = Tello()  # Crea un objeto drone de la clase Tello
    drone.connect()  # Establece conexión con el drone
    drone.streamoff()  # Asegura que el streaming de video esté apagado antes de encenderlo
    drone.streamon()  # Enciende el streaming de video del drone
    # Inicializa velocidades y estados del drone a cero o valores predeterminados
    drone.left_right_velocity = 0  
    drone.forward_backward_velocity = 0
    drone.up_down_velocity = 0
    drone.yaw_velocity = 0
    drone.status = 0  # Estado inicial del drone (0 = en tierra)
    drone.height = 0  # Altura inicial
    drone.speed = 50  # Velocidad de movimiento inicial
    drone.height_lim = 50  # Límite de altura inicial

def no():  # Función placeholder para callbacks de trackbars que no hacen nada
    pass

def pc_f():  # Función para manejar captura de video desde PC (webcam)
    capture = cv2.VideoCapture(0)  # Inicia la captura de video desde la webcam
    while True:
        ret, img = capture.read()  # Lee un frame de la webcam
        img = cv2.flip(img, 1)  # Voltea el frame horizontalmente
        img = cv2.resize(img, (500, 500))  # Redimensiona el frame a 500x500
        cv2.imshow("Image", img)  # Muestra el frame en una ventana

def drone_f():  # Función principal para controlar el drone
    in_speed = 50  # Velocidad inicial
    in_height_lim = 50  # Límite de altura inicial
    cv2.namedWindow('Trackbars')  # Crea una ventana para los trackbars
    cv2.resizeWindow('Trackbars', (500,100))  # Ajusta el tamaño de la ventana de trackbars
    # Crea un trackbar para ajustar la velocidad
    cv2.createTrackbar('Speed', 'Trackbars', 0, 100, no)
    cv2.setTrackbarPos('Speed', 'Trackbars', in_speed)
    # Crea un trackbar para ajustar el límite de altura
    cv2.createTrackbar('Height limit', 'Trackbars', 50, 300, no)
    cv2.setTrackbarPos('Height limit', 'Trackbars', in_height_lim)

    while True:
        # Actualiza los valores de velocidad y altura límite desde los trackbars
        drone.speed = cv2.getTrackbarPos('Speed', 'Trackbars')
        drone.height_lim = cv2.getTrackbarPos('Height limit', 'Trackbars')
        # Comprobación de batería y procedimientos de aterrizaje si la batería es baja
        if drone.status == 1 and drone.get_battery() < 12:
            drone.status = 0
            drone.land()
        frame_read = drone.get_frame_read()  # Lee un frame del video del drone
        img = frame_read.frame
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convierte el frame a color BGR para OpenCV
        img = cv2.flip(img, 1)  # Voltea la imagen horizontalmente
        img = cv2.resize(img, (500, 500))  # Redimensiona la imagen a 500x500
        # Añade texto de nivel de batería en la imagen
        cv2.putText(img, 'Battery:  ' + str(drone.get_battery()), (0, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 3)
        # Añade advertencias de nivel bajo y crítico de batería
        if drone.get_battery() < 25:
            cv2.putText(img, 'Low level', (0, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        if drone.get_battery() <= 15:
            cv2.putText(img, 'Critical level', (0, 90), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        cv2.imshow("Image", img)  # Muestra la imagen modificada en una ventana

        key = cv2.waitKey(45) & 0xFF  # Espera una tecla durante 45 ms
        # Comandos para controlar el drone y la interfaz basados en la tecla presionada
        if key == 113:      #Presionar q para matar el programa.
            cv2.destroyAllWindows()
            if drone.status == 1:
                drone.land()
            drone.streamoff()
            drone.end()
            break
        if key == 116:      #Presionar r para despegar
            if drone.get_battery() >= 25:
                if drone.status == 0:
                    drone.status = 1
                    drone.takeoff()
            else:
                img2 = cv2.imread('fondo.jpg')
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img2, "Battery low", (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow("Warning", img2)
        if key == 108:      #Presionar l para aterrizar
            if drone.status == 1:
                drone.status = 0
                drone.land()
        elif key == 104:    # Presionar h para mantener su posición.
            drone.left_right_velocity = 0 
            drone.forward_backward_velocity = 0
            drone.up_down_velocity = 0
            drone.yaw_velocity = 0
        elif key == 119:    #Presionar w para moverse hacia delante
            drone.left_right_velocity = 0 
            drone.forward_backward_velocity = drone.speed
            drone.up_down_velocity = 0
            drone.yaw_velocity = 0 
        elif key == 115:    #Presionar s para moverse hacia atras. 
            drone.left_right_velocity = 0 
            drone.forward_backward_velocity = -drone.speed
            drone.up_down_velocity = 0
            drone.yaw_velocity = 0
        elif key == 97:     #Presionar a para moverse a la izquierda
            drone.left_right_velocity = -drone.speed
            drone.forward_backward_velocity = 0
            drone.up_down_velocity = 0
            drone.yaw_velocity = 0
        elif key == 100:    #Presionar d para moverse a la derecha
            drone.left_right_velocity = drone.speed
            drone.forward_backward_velocity = 0
            drone.up_down_velocity = 0
            drone.yaw_velocity = 0
        elif key == 101:    #Presionar e para subir.
            drone.left_right_velocity = 0
            drone.forward_backward_velocity = 0
            drone.up_down_velocity = drone.speed
            drone.yaw_velocity = 0
        elif key == 114:    #Presionar r para bajar.
            drone.left_right_velocity = 0
            drone.forward_backward_velocity = 0
            drone.up_down_velocity = -drone.speed
            drone.yaw_velocity = 0
        elif key == 122:    #Presionar z para girar a la izquierda
            drone.left_right_velocity = 0
            drone.forward_backward_velocity = 0
            drone.up_down_velocity = 0
            drone.yaw_velocity = -drone.speed
        elif key == 120:    #Presionar x para girar a la derecha
            drone.left_right_velocity = 0
            drone.forward_backward_velocity = 0
            drone.up_down_velocity = 0
            drone.yaw_velocity = drone.speed
        else:
            drone.left_right_velocity = 0
            drone.forward_backward_velocity = 0
            drone.up_down_velocity = 0
            drone.yaw_velocity = 0
        if (drone.get_height() > drone.height_lim):
            drone.up_down_velocity = -drone.speed
            drone.left_right_velocity = 0
            drone.forward_backward_velocity = 0
            drone.yaw_velocity = 0
        drone.send_rc_control(drone.left_right_velocity, drone.forward_backward_velocity, drone.up_down_velocity, drone.yaw_velocity)


def main():  # Función principal que decide qué función ejecutar basada en frame_source
    print("main program running now")
    if frame_source == 0:
        pc_f()
    elif frame_source == 1:
        drone_f()

try:
    main()  # Intenta ejecutar la función principal
except KeyboardInterrupt:  # Captura interrupción por teclado para cerrar recursos de manera segura
    print('KeyboardInterrupt exception is caught')
    cv2.destroyAllWindows()  # Cierra todas las ventanas de OpenCV
    if frame_source == 1:
        if drone.status == 1:
            drone.land()  # Aterriza el drone si está en vuelo
            drone.streamoff()  # Apaga el streaming de video
            drone.end()  # Finaliza la conexión con el drone
else:
    print('No exceptions are caught')  # Imprime si no se capturan excepciones
