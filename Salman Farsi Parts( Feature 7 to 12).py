def draw_enemy(current_enemy):
    """Draw blue enemy"""
    glPushMatrix()
    glTranslatef(current_enemy.x, current_enemy.y, current_enemy.z)
    
    # Enemy body (blue)
    glColor3f(0, 0, 1)
    glScalef(1.3, 1.3, 2)
    glutSolidCube(25)
    glScalef(1/1.3, 1/1.3, 0.5)
    
    # Enemy head
    glPushMatrix()
    glTranslatef(0, 0,35)
    glColor3f(0, 0, 0.8)
    glutSolidSphere(12,8, 8)
    glPopMatrix()
    
    # Health bar
    glPushMatrix()
    glTranslatef(0, 0, 60)
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    enemy_health_bar_width = (current_enemy.health / current_enemy.max_health) * 25
    glVertex3f(-12, -2, 0)
    glVertex3f(-12 +enemy_health_bar_width, -2, 0)
    glVertex3f(-12+ enemy_health_bar_width, 2, 0)
    glVertex3f(-12, 2, 0)
    glEnd()
    glPopMatrix()
    
    glPopMatrix()

def fire_weapon():
    """Fire weapon from gun barrel"""
    global last_weapon_shot_time, player_projectile_list
    
    if total_frame_count - last_weapon_shot_time > (weapon_shot_cooldown * 60):
        # Calculate gun barrel position (chest level, front of player)
        gun_barrel_x = player_world_position[0]+35 *math.cos(math.radians(player_body_rotation))
        gun_barrel_y = player_world_position[1]+ 35*math.sin(math.radians(player_body_rotation))
        gun_barrel_z = player_world_position[2]+ 5  
        # Projectile velocity in direction player is facing
        projectile_velocity_x = 300 * math.cos(math.radians(player_body_rotation))
        projectile_velocity_y = 300 * math.sin(math.radians(player_body_rotation))
        player_projectile_list.append({
            'x': gun_barrel_x, 'y': gun_barrel_y, 'z': gun_barrel_z,
            'vx': projectile_velocity_x, 'vy': projectile_velocity_y, 'vz': 0, 'life':120
        })
        
        last_weapon_shot_time = total_frame_count

def fire_at_enemy(target_enemy):
    """Fire weapon directly at specific enemy (for cheat mode)"""
    global last_weapon_shot_time, player_projectile_list
    
    # Calculate gun barrel position
    gun_barrel_x = player_world_position[0] +35* math.cos(math.radians(player_body_rotation))
    gun_barrel_y = player_world_position[1]+ 35 *math.sin(math.radians(player_body_rotation))
    gun_barrel_z = player_world_position[2] +5
    
    # Calculate direction to enemy
    enemy_direction_x=target_enemy.x-gun_barrel_x
    enemy_direction_y= target_enemy.y -gun_barrel_y
    enemy_distance =math.sqrt(enemy_direction_x*enemy_direction_x + enemy_direction_y*enemy_direction_y)
    
    if enemy_distance > 0:
        targeted_velocity_x=(enemy_direction_x / enemy_distance) * 300
        targeted_velocity_y=(enemy_direction_y / enemy_distance) * 300
        
        player_projectile_list.append({
            'x': gun_barrel_x, 'y': gun_barrel_y, 'z': gun_barrel_z,
            'vx': targeted_velocity_x, 'vy': targeted_velocity_y, 'vz': 0, 'life': 120
        })
        
        last_weapon_shot_time=total_frame_count

def update_projectiles():
    """Update all projectiles and handle collisions"""
    global player_projectile_list, enemy_projectile_list, enemy_list, palace_current_health, player_current_health
    
    physics_delta_time=1.0/60.0
    
    # Update player projectiles
    for player_projectile in player_projectile_list[:]:
        player_projectile['x']+=player_projectile['vx'] * physics_delta_time
        player_projectile['y'] += player_projectile['vy'] * physics_delta_time
        player_projectile['life']-=1
        
        if player_projectile['life']<=0:
            player_projectile_list.remove(player_projectile)
            continue
            
        # Check colliion with enemies
        for enemy_target in enemy_list[:]:
            collision_distance_x=player_projectile['x'] - enemy_target.x
            collision_distance_y=player_projectile['y'] - enemy_target.y
            collision_distance_z=player_projectile['z'] - enemy_target.z
            if collision_distance_x*collision_distance_x + collision_distance_y*collision_distance_y + collision_distance_z*collision_distance_z < 900:
                enemy_target.health-=2  # Enemy health reduces by 2
                if player_projectile in player_projectile_list:
                    player_projectile_list.remove(player_projectile)
                if enemy_target.health<= 0:
                    enemy_list.remove(enemy_target)
                break
    
    # Update enemy projectiles
    for enemy_projectile in enemy_projectile_list[:]:
        enemy_projectile['x']+=enemy_projectile['vx'] * physics_delta_time
        enemy_projectile['y']+=enemy_projectile['vy'] * physics_delta_time
        enemy_projectile['life']-=1
        
        if enemy_projectile['life']<=0:
            enemy_projectile_list.remove(enemy_projectile)
            continue
        
        # Check what the projectile is targeting
        if enemy_projectile['target'] == 'palace':
            # Check collision with palace
            palace_collision_x=enemy_projectile['x'] - palace_world_position[0]
            palace_collision_y=enemy_projectile['y'] - palace_world_position[1]
            palace_collision_z=enemy_projectile['z'] - palace_world_position[2]
            if palace_collision_x*palace_collision_x + palace_collision_y*palace_collision_y + palace_collision_z*palace_collision_z < 2500: 
                palace_current_health-=1 
                if enemy_projectile in enemy_projectile_list:
                    enemy_projectile_list.remove(enemy_projectile)
        else:  
            # Check collision with player
            player_collision_x = enemy_projectile['x']-player_world_position[0]
            player_collision_y = enemy_projectile['y']- player_world_position[1]
            player_collision_z = enemy_projectile['z']-player_world_position[2]
            if player_collision_x*player_collision_x+player_collision_y*player_collision_y +player_collision_z*player_collision_z <400:  
                player_current_health-=1 
                if enemy_projectile in enemy_projectile_list:
                    enemy_projectile_list.remove(enemy_projectile)

def draw_projectile(current_projectile, is_enemy_projectile=False):
    """Draw projectiles"""
    glPushMatrix()
    glTranslatef(current_projectile['x'], current_projectile['y'], current_projectile['z'])
    if is_enemy_projectile:
        glColor3f(1, 0.2, 0.2) 
    else:
        glColor3f(0.2, 1, 0.2)      
    glutSolidSphere(3, 6, 6)
    glPopMatrix()

def draw_palace():
    """Draw a small palace structure"""
    glPushMatrix()
    glTranslatef(palace_world_position[0], palace_world_position[1], palace_world_position[2])
    
    # Palace base
    glColor3f(0.8, 0.7, 0.5)  
    glScalef(2, 2, 1)
    glutSolidCube(40)
    glScalef(0.5, 0.5, 1)
    
    # Palace towers 
    for tower_x in [-1, 1]:
        for tower_y in [-1, 1]:
            glPushMatrix()
            glTranslatef(tower_x * 35, tower_y * 35, 30)
            glColor3f(0.7, 0.6, 0.4)
            glScalef(0.6, 0.6, 1.5)
            glutSolidCube(25)
            glPopMatrix()
    
    # Central dome
    glPushMatrix()
    glTranslatef(0, 0,50)
    glColor3f(0.9,0.8, 0.6)
    glutSolidSphere(20, 12, 12)
    glPopMatrix()
    
    # Health bar above palace
    glPushMatrix()
    glTranslatef(0,0, 80)
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    health_bar_width =(palace_current_health / palace_maximum_health) * 60
    glVertex3f(-30, -5, 0)
    glVertex3f(-30 + health_bar_width, -5, 0)
    glVertex3f(-30 + health_bar_width, 5, 0)
    glVertex3f(-30, 5, 0)
    glEnd()
    glPopMatrix()
    
    glPopMatrix()

def execute_cheat_mode():
    """FIXED: Execute enhanced cheat mode sequence with visual movement"""
    global is_cheat_mode_active, cheat_current_step, cheat_mode_timer, player_blocks_inventory, player_world_position, player_body_rotation
    global cheat_target_block_ref, cheat_blocks_collected_count, cheat_target_blocks_needed
    
    if not is_cheat_mode_active:
        return
    
    cheat_mode_timer+=1
    
    if cheat_current_step == 0:  # Collect blocks by moving to them
        if cheat_target_block_ref is None or cheat_target_block_ref.collected:
            cheat_target_block_ref = find_nearest_uncollected_block()
            
        if cheat_target_block_ref is not None:
            # Move toward target block
            target_direction_x = cheat_target_block_ref.x - player_world_position[0]
            target_direction_y = cheat_target_block_ref.y - player_world_position[1]
            target_distance = math.sqrt(target_direction_x*target_direction_x + target_direction_y*target_direction_y)
            
            if target_distance > 25:  
                cheat_movement_speed = 6 
                player_world_position[0] += (target_direction_x / target_distance) * cheat_movement_speed
                player_world_position[1] += (target_direction_y / target_distance) * cheat_movement_speed
                

                player_body_rotation = math.degrees(math.atan2(target_direction_y, target_direction_x))
            else:
                # Collected the block
                cheat_target_block_ref.collected = True
                player_blocks_inventory += 1
                cheat_blocks_collected_count += 1
                cheat_target_block_ref = None  
                
                if cheat_blocks_collected_count >= cheat_target_blocks_needed:
                    cheat_current_step = 1  
                    cheat_mode_timer = 0
        else:
            # No more blocks, move to palace
            cheat_current_step = 1
            cheat_mode_timer = 0
    
    elif cheat_current_step==1:  # Move to palace
        # Move player toward palace
        palace_direction_x=palace_world_position[0] - player_world_position[0]
        palace_direction_y=palace_world_position[1] - player_world_position[1]
        palace_distance = math.sqrt(palace_direction_x*palace_direction_x + palace_direction_y*palace_direction_y)
        
        if palace_distance > 80:  # Not at palace yet
            palace_movement_speed = 8       
            player_world_position[0] += (palace_direction_x / palace_distance) * palace_movement_speed
            player_world_position[1] += (palace_direction_y / palace_distance) * palace_movement_speed
            
            # Rotate player to face the palace
            player_body_rotation = math.degrees(math.atan2(palace_direction_y, palace_direction_x))
        else:
            cheat_current_step=2  # Redeem blocks phase
            cheat_mode_timer=0
    
    elif cheat_current_step==2:  # Redeem blocks at palace
        if cheat_mode_timer>30: 
            while player_blocks_inventory> 0:
                place_block_at_palace()  # Redeem all blocks
            cheat_current_step=3  # Start shooting phase
            cheat_mode_timer=0
    
    elif cheat_current_step==3:  # Shoot at enemies
        if cheat_mode_timer>10: 
            # Find and shoot at all enemies
            for enemy_to_shoot in enemy_list[:]:
                fire_at_enemy(enemy_to_shoot)
            # Reset cheat mode
            is_cheat_mode_active =False
            cheat_current_step=0
            cheat_mode_timer=0
            cheat_blocks_collected_count =0
            cheat_target_block_ref=None

def find_nearest_uncollected_block():
    """Find the nearest uncolleted block to the player"""
    nearest_block_ref=None
    minimum_distance=float('inf')
    
    for scattered_block in collectible_blocks_list:
        if not scattered_block.collected:
            block_distance_x=scattered_block.x-player_world_position[0]
            block_distance_y =scattered_block.y -player_world_position[1]
            block_distance =math.sqrt(block_distance_x*block_distance_x + block_distance_y*block_distance_y)
            
            if block_distance<minimum_distance:
                minimum_distance =block_distance
                nearest_block_ref=scattered_block
    
    return nearest_block_ref

def reset_game_to_defaults():
    """ Reset all game variables to default values"""
    global current_game_phase, current_wave_number, enemy_list, player_projectile_list, enemy_projectile_list
    global player_blocks_inventory, collectible_blocks_list, player_placed_blocks, player_current_health, palace_current_health, palace_maximum_health
    global player_world_position, player_body_rotation, camera_rotation_angle, camera_vertical_height, current_phase_timer
    global is_cheat_mode_active, cheat_current_step, cheat_mode_timer, cheat_target_block_ref, cheat_blocks_collected_count
    global is_first_person_mode, last_weapon_shot_time, total_frame_count
    
    # Reset game state
    current_game_phase=GamePhase.BUILDING
    current_wave_number= DEFAULT_CURRENT_WAVE_NUMBER
    
    # Clear all lists
    enemy_list.clear()
    player_projectile_list.clear()
    enemy_projectile_list.clear()
    collectible_blocks_list.clear()
    player_placed_blocks.clear()
    
    # Reset player
    player_world_position =[DEFAULT_PLAYER_WORLD_POS[0], DEFAULT_PLAYER_WORLD_POS[1], DEFAULT_PLAYER_WORLD_POS[2]]
    player_body_rotation= DEFAULT_PLAYER_BODY_ROTATION
    player_current_health =DEFAULT_PLAYER_CURRENT_HEALTH
    
    # Reset palace
    palace_current_health=DEFAULT_PALACE_CURRENT_HEALTH
    palace_maximum_health = DEFAULT_PALACE_MAXIMUM_HEALTH
    
    # Reset camera
    camera_rotation_angle =DEFAULT_CAMERA_ROTATION_ANGLE
    camera_vertical_height= DEFAULT_CAMERA_VERTICAL_HEIGHT
    is_first_person_mode =False
    
    # Reset inventory and blocks
    player_blocks_inventory= 0
    
    # Reset cheat mode
    is_cheat_mode_active= False
    cheat_current_step =0
    cheat_mode_timer=0
    cheat_target_block_ref=None
    cheat_blocks_collected_count= 0
    
    # Reset timers
    current_phase_timer = building_phase_duration * 60
    last_weapon_shot_time = 0
    
    # Spawn initial blocks
    spawn_scattered_blocks()