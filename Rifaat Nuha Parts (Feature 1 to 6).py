
def keyboardListener(pressed_key, mouse_x, mouse_y):
    global player_world_position, player_body_rotation, current_game_phase, current_wave_number, player_current_health, palace_current_health, current_phase_timer
    global is_cheat_mode_active, cheat_current_step, cheat_mode_timer
    
    # Only allow movement if not in cheat mode
    if not is_cheat_mode_active:
        # Movement - player moves in direction they're facing
        if pressed_key == b'w':  # Move forward
            player_world_position[0] += 5 * math.cos(math.radians(player_body_rotation))
            player_world_position[1] += 5 * math.sin(math.radians(player_body_rotation))
            
        elif pressed_key == b's':  # Move backward  
            player_world_position[0]-=5*math.cos(math.radians(player_body_rotation))
            player_world_position[1] -=5*math.sin(math.radians(player_body_rotation))
            
        elif pressed_key== b'a':  # Rotate left (whole body)
            player_body_rotation += 5
            
        elif pressed_key==b'd':  # Rotate right (whole body)
            player_body_rotation-= 5
        
    # NEW: Cheat mode activation
    if pressed_key==b'c':
        if not is_cheat_mode_active:
            is_cheat_mode_active=True
            cheat_current_step=0
            cheat_mode_timer=0
            cheat_target_block_ref=None
            cheat_blocks_collected_count=0
        
    # FIXED: Reset game with all defaults
    elif pressed_key==b'r':
        reset_game_to_defaults()




def draw_robot_player():
    """Draw robot player with gun at chest level"""
    if is_first_person_mode:
        return
        
    glPushMatrix()
    glTranslatef(player_world_position[0], player_world_position[1], player_world_position[2])
    glRotatef(player_body_rotation, 0, 0, 1)  # Rotate entire body



    # Torso (yellow)
    glPushMatrix()
    glColor3f(1, 1, 0)
    glScalef(1, 1, 1.5)
    glutSolidCube(20)
    glPopMatrix()



    # Head (black)
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glColor3f(0, 0, 0)
    glutSolidSphere(8, 8, 8)
    # Eyes
    glColor3f(1, 0, 0)
    glTranslatef(5, 0, 2)
    glutSolidSphere(2, 4, 4)
    glTranslatef(-10, 0, 0)
    glutSolidSphere(2, 4, 4)
    glPopMatrix()
    
    # Arms (black)
    glPushMatrix()
    glTranslatef(15, 0, 5)
    glColor3f(0, 0, 0)
    glScalef(0.5, 0.5, 1.2)
    glutSolidCube(12)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-15, 0, 5)
    glColor3f(0, 0, 0)
    glScalef(0.5, 0.5, 1.2)
    glutSolidCube(12)
    glPopMatrix()
    
    # Legs (black)
    glPushMatrix()
    glTranslatef(6, 0, -25)
    glColor3f(0, 0, 0)
    glScalef(0.6, 0.6, 1.5)
    glutSolidCube(12)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-6, 0, -25)
    glColor3f(0, 0, 0)
    glScalef(0.6, 0.6, 1.5)
    glutSolidCube(12)
    glPopMatrix()
    
    # Gun at  levl
    glPushMatrix()
    glTranslatef(20, 0, 5)  
    glColor3f(0.2, 0.2, 0.2)
    glScalef(2, 0.3, 0.3)
    glutSolidCube(15)
    glPopMatrix()
    
    glPopMatrix()

def mouseListener(mouse_button, button_state, click_x, click_y):
    global is_first_person_mode
    
    if mouse_button==GLUT_LEFT_BUTTON and button_state == GLUT_DOWN:
        # NEW: Toggle camera mode on left click
        is_first_person_mode = not is_first_person_mode
    elif mouse_button == GLUT_RIGHT_BUTTON and button_state == GLUT_DOWN:
        # Only allow manual actions if not in cheat mode
        if not is_cheat_mode_active:
            # Check if near palace to place block, otherwise shoot
            palace_interaction_distance_x = palace_world_position[0] - player_world_position[0]
            palace_interaction_distance_y = palace_world_position[1] - player_world_position[1]
            palace_interaction_distance = math.sqrt(palace_interaction_distance_x*palace_interaction_distance_x + palace_interaction_distance_y*palace_interaction_distance_y)
            
            if palace_interaction_distance < 100:  
                place_block_at_palace()
            else:  
                fire_weapon()

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(camera_field_of_view,1.25, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if is_first_person_mode:
        # NEW: First person camera - position at player's eye level
        player_eye_height=player_world_position[2] + 20  # Eye level above player
        camera_look_x=player_world_position[0]+100*math.cos(math.radians(player_body_rotation))
        camera_look_y=player_world_position[1]+100*math.sin(math.radians(player_body_rotation))
        
        gluLookAt(player_world_position[0],player_world_position[1], player_eye_height,  # Camera at player position
                  camera_look_x, camera_look_y, player_eye_height,  
                  0, 0, 1)  
    else:
        # Original third person camera
        camera_orbit_radius = 600
        camera_world_x=camera_orbit_radius *math.cos(math.radians(camera_rotation_angle))
        camera_world_y=camera_orbit_radius*math.sin(math.radians(camera_rotation_angle))
        
        gluLookAt(camera_world_x, camera_world_y, camera_vertical_height,
                  0, 0, 0,
                  0, 0, 1)

def specialKeyListener(special_key,mouse_x, mouse_y):
    global camera_vertical_height,camera_rotation_angle
    
    if special_key==GLUT_KEY_UP:
        camera_vertical_height+=20
        if camera_vertical_height>800:
            camera_vertical_height=800
    elif special_key==GLUT_KEY_DOWN:
        camera_vertical_height -= 20
        if camera_vertical_height <100:
            camera_vertical_height= 100
    elif special_key == GLUT_KEY_LEFT:
        camera_rotation_angle +=5
    elif special_key == GLUT_KEY_RIGHT:
        camera_rotation_angle-=5



def check_block_collection():
    """Check if player collides with any scattered blocks"""
    global player_blocks_inventory, collectible_blocks_list
    for collectible_block in collectible_blocks_list:
        if not collectible_block.collected:
            distance_x =collectible_block.x - player_world_position[0]
            distance_y=collectible_block.y - player_world_position[1]
            collision_distance=math.sqrt(distance_x*distance_x + distance_y*distance_y)    
            if collision_distance <25:  
                collectible_block.collected = True
                player_blocks_inventory+= 1




def spawn_scattered_blocks():
    """Spawn blocks randomly around the map for collection"""
    global collectible_blocks_list
    collectible_blocks_list.clear()
    
    for block_index in range(15):  
        spawn_angle = random.random() * 2 * math.pi
        spawn_distance = random.uniform(200, 500)
        spawn_x = spawn_distance * math.cos(spawn_angle)
        spawn_y = spawn_distance * math.sin(spawn_angle)
        spawn_z = 20       
        collectible_blocks_list.append(Block(spawn_x, spawn_y, spawn_z, True))




def draw_scattered_block(scattered_block):
    """Draw collectible blocks scattered around"""
    if not scattered_block.collected:
        glPushMatrix()
        glTranslatef(scattered_block.x, scattered_block.y, scattered_block.z)
        glRotatef(total_frame_count * 2, 0, 0, 1)   
        glColor3f(0.5, 0.8, 0.3) 
        glutSolidCube(15)    
        glPopMatrix()

def place_block_at_palace():
    """Place block at palace if player is near and has blocks"""
    global player_blocks_inventory, palace_current_health, palace_maximum_health
    
    # Check if player is near palace
    palace_distance_x=palace_world_position[0] -player_world_position[0]
    palace_distance_y=palace_world_position[1]-player_world_position[1]
    palace_distance=math.sqrt(palace_distance_x*palace_distance_x + palace_distance_y*palace_distance_y)
    
    if palace_distance<100 and player_blocks_inventory> 0:  # Within range and has blocks
        player_blocks_inventory-=1
        palace_current_health =min(palace_current_health +10, palace_maximum_health + (player_blocks_inventory * 5))
        palace_maximum_health=max(palace_maximum_health, palace_current_health)







def update_game_logic():
    """Update main game logic"""
    global current_game_phase,current_phase_timer, current_wave_number
    
    # Only do normal collection if not in cheat mode
    if not is_cheat_mode_active:
        check_block_collection()  # Automatically collect blocks
    
    execute_cheat_mode()  
    
    if current_game_phase==GamePhase.BUILDING:
        current_phase_timer-=1
        
        if current_phase_timer<=0:
            current_game_phase=GamePhase.ATTACKING
            current_phase_timer= attack_phase_duration * 60
            spawn_enemies()
            
    elif current_game_phase==GamePhase.ATTACKING:
        # Update enemies and make them shoot based on their target
        for current_enemy in enemy_list:
            current_enemy.move_toward_player()
            
            if total_frame_count % int(60 * current_enemy.shot_cooldown) == 0:
                if current_enemy.target_type == 'palace':
                    current_enemy.shoot_at_palace()
                else:  
                    current_enemy.shoot_at_player()
                
        current_phase_timer -= 1
        
        if len(enemy_list) == 0 or current_phase_timer <= 0:
            current_wave_number += 1
            current_game_phase = GamePhase.BUILDING
            current_phase_timer = building_phase_duration * 60
            spawn_scattered_blocks()  
            
    # Check game over
    if player_current_health <=0 or palace_current_health<= 0:
        current_game_phase =GamePhase.GAME_OVER
        
    update_projectiles()



    
def spawn_enemies():
    """Spawn enemies at random positions"""
    global enemy_list
    enemy_list.clear()
    
    # Spawn first enemy that targets palace
    enemy_spawn_angle1=random.random()*2*math.pi
    enemy_spawn_distance=400
    enemy_x1=enemy_spawn_distance*math.cos(enemy_spawn_angle1)
    enemy_y1=enemy_spawn_distance*math.sin(enemy_spawn_angle1)
    enemy_list.append(Enemy(enemy_x1,enemy_y1,'palace'))
    


    # Spawn second enemy that targets player
    enemy_spawn_angle2=random.random() * 2 * math.pi
    enemy_x2=enemy_spawn_distance * math.cos(enemy_spawn_angle2)
    enemy_y2=enemy_spawn_distance * math.sin(enemy_spawn_angle2)
    enemy_list.append(Enemy(enemy_x2,enemy_y2, 'player'))
