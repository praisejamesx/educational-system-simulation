import pygame
import numpy as np
import matplotlib.pyplot as plt
import sys

class EducationalSystemSimulation:
    def __init__(self, num_students=25):
        self.num_students = num_students
        self.setup_parameters()
        self.setup_pygame()
        self.setup_students()
        self.history = []
        
        # Setup matplotlib in interactive mode
        plt.ion()
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 5))
        plt.subplots_adjust(wspace=0.3)
        
    def setup_parameters(self):
        # Initial students parameters
        self.curriculum_content = 80
        self.time_allotted = 70
        self.teacher_skill = 0.85
        self.passing_threshold = 1.0
        
        # Control ranges for sliders
        self.param_ranges = {
            'class_size': (5, 40),
            'teacher_skill': (0.1, 1.0),
            'curriculum_intensity': (50, 200),
            'time_available': (30, 120)
        }
        
    def class_size_penalty(self, n):
        """Penalty factor for larger class sizes"""
        return 1 + 0.025 * (n - 1)
    
    def compute_effective_demand(self):
        """Calculate the system's effective demand on students"""
        base_pace = self.curriculum_content / self.time_allotted
        teacher_factor = 1.0 / self.teacher_skill
        size_penalty = self.class_size_penalty(self.num_students)
        
        return base_pace * teacher_factor * size_penalty
    
    def compute_capacity_ratio(self, learning_speed):
        """Calculate individual student's capacity ratio"""
        demand = self.compute_effective_demand()
        return learning_speed / demand
    
    def probability_of_passing(self, capacity_ratio, sharpness=5):
        """Smooth probability function using logistic curve"""
        return 1 / (1 + np.exp(-sharpness * (capacity_ratio - self.passing_threshold)))
    
    def setup_students(self):
        """Initialize student population with varied learning speeds"""
        self.learning_speeds = np.random.normal(loc=1.1, scale=0.25, size=self.num_students)
        # Ensure no negative learning speeds
        self.learning_speeds = np.maximum(0.3, self.learning_speeds)
        
        # Random positions for visualization
        self.student_positions = [
            (np.random.randint(40, 360), np.random.randint(60, 340))
            for _ in range(self.num_students)
        ]
    
    def setup_pygame(self):
        """Initialize Pygame components within small window"""
        pygame.init()
        self.screen = pygame.display.set_mode((400, 500))
        pygame.display.set_caption("Education System Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 22)
        self.small_font = pygame.font.Font(None, 18)
        
        # Create sliders
        self.sliders = {
            'class_size': {'value': self.num_students, 'rect': pygame.Rect(20, 410, 160, 15), 'dragging': False},
            'teacher_skill': {'value': self.teacher_skill, 'rect': pygame.Rect(20, 435, 160, 15), 'dragging': False},
            'curriculum_intensity': {'value': self.curriculum_content, 'rect': pygame.Rect(20, 460, 160, 15), 'dragging': False},
            'time_available': {'value': self.time_allotted, 'rect': pygame.Rect(20, 485, 160, 15), 'dragging': False}
        }
    
    def update_parameters(self):
        """Update simulation parameters from sliders"""
        self.num_students = int(self.sliders['class_size']['value'])
        self.teacher_skill = self.sliders['teacher_skill']['value']
        self.curriculum_content = self.sliders['curriculum_intensity']['value']
        self.time_allotted = self.sliders['time_available']['value']
        
        # Update student population if class size changed
        if len(self.learning_speeds) != self.num_students:
            self.setup_students()
    
    def draw_slider(self, name, y_pos, label, min_val, max_val):
        """Draw a slider control"""
        slider = self.sliders[name]
        rect = slider['rect']
        
        # Draw slider track
        pygame.draw.rect(self.screen, (80, 80, 80), rect, border_radius=2)
        pygame.draw.rect(self.screen, (120, 120, 120), rect, 1, border_radius=2)
        
        # Calculate handle position
        handle_x = rect.left + (slider['value'] - min_val) / (max_val - min_val) * rect.width
        handle_rect = pygame.Rect(handle_x - 4, rect.top - 3, 8, 21)
        
        # Draw handle
        color = (220, 120, 120) if slider['dragging'] else (200, 200, 200)
        pygame.draw.rect(self.screen, color, handle_rect, border_radius=2)
        pygame.draw.rect(self.screen, (100, 100, 100), handle_rect, 1, border_radius=2)
        
        # Draw label and value
        label_text = f"{label}: {slider['value']:.1f}"
        text_surf = self.small_font.render(label_text, True, (255, 255, 255))
        self.screen.blit(text_surf, (rect.right + 8, rect.top - 4))
    
    def update_matplotlib_plot(self):
        """Update the matplotlib plots in separate window"""
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Calculate current data
        capacity_ratios = [self.compute_capacity_ratio(speed) for speed in self.learning_speeds]
        
        # Plot 1: Capacity ratio distribution
        colors = ['green' if cr >= self.passing_threshold else 'red' for cr in capacity_ratios]
        n, bins, patches = self.ax1.hist(capacity_ratios, bins=8, alpha=0.7, color='lightblue', edgecolor='black')
        
        # Color individual bars based on threshold
        for i, (patch, bin_edge) in enumerate(zip(patches, bins)):
            if bin_edge < self.passing_threshold:
                patch.set_facecolor('lightcoral')
            else:
                patch.set_facecolor('lightgreen')
        
        self.ax1.axvline(self.passing_threshold, color='red', linestyle='--', linewidth=2, label='Passing Threshold')
        self.ax1.set_xlabel('Capacity Ratio')
        self.ax1.set_ylabel('Number of Students')
        self.ax1.set_title('Distribution of Student Capacity Ratios')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        
        # Plot 2: Fail rate history
        if len(self.history) > 0:
            fail_rates = [h['fail_rate'] for h in self.history]
            time_steps = range(len(fail_rates))
            self.ax2.plot(time_steps, fail_rates, 'r-', linewidth=2, label='Fail Rate')
            self.ax2.fill_between(time_steps, fail_rates, alpha=0.3, color='red')
            self.ax2.set_ylim(0, 100)
            self.ax2.set_xlabel('Time Steps')
            self.ax2.set_ylabel('Fail Rate (%)')
            self.ax2.set_title('Fail Rate Over Time')
            self.ax2.legend()
            self.ax2.grid(True, alpha=0.3)
        
        # Update the plots
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def run(self):
        """Main simulation loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle slider dragging
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for name, slider in self.sliders.items():
                        handle_x = slider['rect'].left + (slider['value'] - self.param_ranges[name][0]) / (
                            self.param_ranges[name][1] - self.param_ranges[name][0]) * slider['rect'].width
                        handle_rect = pygame.Rect(handle_x - 4, slider['rect'].top - 3, 8, 21)
                        
                        if handle_rect.collidepoint(event.pos):
                            slider['dragging'] = True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    for slider in self.sliders.values():
                        slider['dragging'] = False
                
                if event.type == pygame.MOUSEMOTION:
                    for name, slider in self.sliders.items():
                        if slider['dragging']:
                            rel_x = max(0, min(event.pos[0] - slider['rect'].left, slider['rect'].width))
                            proportion = rel_x / slider['rect'].width
                            min_val, max_val = self.param_ranges[name]
                            slider['value'] = min_val + proportion * (max_val - min_val)
            
            # Update simulation
            self.update_parameters()
            
            # Calculate current state
            capacity_ratios = [self.compute_capacity_ratio(speed) for speed in self.learning_speeds]
            fail_count = sum(1 for cr in capacity_ratios if cr < self.passing_threshold)
            fail_rate = (fail_count / self.num_students) * 100
            
            # Record history
            self.history.append({
                'fail_rate': fail_rate,
                'avg_capacity_ratio': np.mean(capacity_ratios),
                'demand': self.compute_effective_demand()
            })
            
            # Keep history manageable
            if len(self.history) > 50:
                self.history.pop(0)
            
            # Draw everything in Pygame
            self.screen.fill((35, 35, 45))  # Dark blue-gray background
            
            # Draw title and model equation
            title_text = self.font.render("Educational System Simulation", True, (255, 255, 200))
            self.screen.blit(title_text, (20, 10))
            
            eq_text = self.small_font.render("Capacity Ratio = Learning Speed / Effective Demand", True, (200, 200, 255))
            self.screen.blit(eq_text, (20, 35))
            
            # Draw students in main area
            for i, (pos, cr) in enumerate(zip(self.student_positions, capacity_ratios)):
                # Color based on capacity ratio with smooth gradient
                if cr >= self.passing_threshold:
                    # Green for passing - brighter green for higher ratios
                    green_intensity = 150 + min(105, int(105 * (cr - self.passing_threshold)))
                    color = (0, green_intensity, 0)
                else:
                    # Red for failing - brighter red for worse ratios
                    severity = min(1.0, (self.passing_threshold - cr) / self.passing_threshold)
                    red_intensity = 150 + int(105 * severity)
                    color = (red_intensity, 0, 0)
                
                pygame.draw.circle(self.screen, color, pos, 6)
                pygame.draw.circle(self.screen, (255, 255, 255), pos, 6, 1)  # White border
                
                # Show capacity ratio as text near student (smaller)
                cr_text = self.small_font.render(f"{cr:.1f}", True, (255, 255, 255))
                text_rect = cr_text.get_rect(center=(pos[0], pos[1] + 15))
                self.screen.blit(cr_text, text_rect)
            
            # Draw info panel
            info_bg_rect = pygame.Rect(220, 60, 170, 340)
            pygame.draw.rect(self.screen, (50, 50, 60), info_bg_rect, border_radius=5)
            pygame.draw.rect(self.screen, (100, 100, 120), info_bg_rect, 1, border_radius=5)
            
            info_y = 70
            info_lines = [
                "SYSTEM STATUS",
                f"Students: {self.num_students}",
                f"Teacher Skill: {self.teacher_skill:.2f}",
                f"Curriculum: {self.curriculum_content:.0f}",
                f"Time: {self.time_allotted:.0f} min",
                f"Demand: {self.compute_effective_demand():.2f}",
                "",
                "RESULTS",
                f"Fail Rate: {fail_rate:.1f}%",
                f"Avg Ratio: {np.mean(capacity_ratios):.2f}",
                f"Passing: {self.num_students - fail_count}/{self.num_students}",
                "",
                "CONTROLS",
                "< Drag sliders >",
                "to adjust parameters"
            ]
            
            for i, line in enumerate(info_lines):
                color = (255, 255, 200) if i in [0, 7, 12] else (255, 255, 255)
                text_surf = self.small_font.render(line, True, color)
                self.screen.blit(text_surf, (230, info_y))
                info_y += 20 if i in [0, 6, 11, 12] else 18
            
            # Draw sliders
            slider_title = self.small_font.render("Adjust System Parameters:", True, (255, 255, 200))
            self.screen.blit(slider_title, (20, 390))
            
            self.draw_slider('class_size', 410, "Class Size", 5, 40)
            self.draw_slider('teacher_skill', 435, "Teacher Skill", 0.1, 1.0)
            self.draw_slider('curriculum_intensity', 460, "Curriculum", 50, 200)
            self.draw_slider('time_available', 485, "Time", 30, 120)
            
            # Update matplotlib plots
            self.update_matplotlib_plot()
            
            pygame.display.flip()
            self.clock.tick(30)
        
        plt.close()
        pygame.quit()
        sys.exit()

# Run the simulation
if __name__ == "__main__":
    print("Starting Educational System Simulation...")
    sim = EducationalSystemSimulation()
    sim.run()