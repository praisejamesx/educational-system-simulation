# Educational System Simulation
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

A simple Python simulation that models educational system dynamics using capacity ratio analysis. This implementation visualizes how systemic factors (class size, teacher skill, curriculum intensity, time constraints) affect student outcomes through Pygame visualization and Matplotlib analytics. It was created for illustrating my essay: 


![Simulation Screenshot](simulation_screenshot.png)

## Mathematical Model


The simulation implements a capacity ratio model:

\[
CR_i = \frac{r_i}{\frac{C}{T} \times \frac{1}{S} \times P(N)}
\]

Where:
- \( CR_i \): Student \( i \)'s capacity ratio  
- \( r_i \): Individual learning speed
- \( C/T \): Curriculum content per time
- \( S \): Teacher skill (0-1)
- \( P(N) \): Class size penalty (\( 1 + 0.025(N-1) \))

Students pass when \( CR_i \geq 1 \), fail when \( CR_i < 1 \).


## System Architecture

### Core Components

```
EducationalSystemSimulation
├── __init__() - Initializes simulation parameters and UI
├── setup_parameters() - Configures default values and ranges
├── setup_pygame() - Initializes visualization window
├── setup_students() - Creates student population
├── run() - Main simulation loop
└── Helper Methods
    ├── compute_effective_demand()
    ├── compute_capacity_ratio()
    ├── probability_of_passing()
    ├── update_matplotlib_plot()
    └── draw_slider()
```

### Class Structure

```python
class EducationalSystemSimulation:
    # Core attributes
    num_students: int
    curriculum_content: float
    time_allotted: float
    teacher_skill: float
    passing_threshold: float
    
    # UI components
    screen: pygame.Surface
    sliders: dict
    font: pygame.font.Font
    
    # Data storage
    learning_speeds: np.array
    student_positions: list
    history: list
```

## Installation & Dependencies

### Requirements

```bash
python>=3.8
pygame>=2.0.0
numpy>=1.20.0
matplotlib>=3.5.0
```

### Installation

```bash
# Clone repository
git clone https://github.com/praisejamesx/educational-system-simulation.git

cd educational-system-simulation

# install dependencies
pip install -r requirements.txt

# Run simulation
python simulation.py
```

## Parameter Configuration

### Default Values

| Parameter | Default Value | Range | Description |
|-----------|---------------|--------|-------------|
| Class Size | 25 students | 5-40 | Number of students in class |
| Teacher Skill | 0.85 | 0.1-1.0 | Teaching effectiveness (higher = better) |
| Curriculum Intensity | 80 units | 50-200 | Amount of content to cover |
| Time Available | 70 minutes | 30-120 | Total instructional time |
| Passing Threshold | 1.0 | Fixed | Minimum capacity ratio to pass |

### Class Size Penalty Function

```python
def class_size_penalty(self, n):
    return 1 + 0.025 * (n - 1)
```
- Linear penalty scaling with class size
- Each additional student adds 2.5% to effective demand

## User Interface

### Pygame Window (400×500 pixels)

**Main Visualization Area:**
- Students represented as colored circles
- Green: Passing (CR ≥ 1.0)
- Red: Failing (CR < 1.0)
- White text shows individual capacity ratios

**Information Panel:**
- Real-time system status
- Current results and statistics
- Control instructions

**Interactive Sliders:**
- Class Size (5-40 students)
- Teacher Skill (0.1-1.0)
- Curriculum Intensity (50-200 units)
- Time Available (30-120 minutes)

### Matplotlib Window

**Plot 1: Capacity Ratio Distribution**
- Histogram of student capacity ratios
- Red dashed line at passing threshold
- Color-coded bars (red below, green above threshold)

**Plot 2: Fail Rate Over Time**
- Real-time tracking of failure percentage
- 50-step moving history window
- Red line with shaded fill

## Simulation Dynamics

### Student Population Generation

```python
# Learning speeds follow normal distribution
self.learning_speeds = np.random.normal(loc=1.1, scale=0.25, size=self.num_students)
self.learning_speeds = np.maximum(0.3, self.learning_speeds)  # No negative values
```

- **Mean Learning Speed**: 1.1 units/minute
- **Standard Deviation**: 0.25 units/minute
- **Minimum Speed**: 0.3 units/minute

### Real-time Updates

1. **Parameter Changes**: Slider adjustments immediately recalculate all capacity ratios
2. **Visual Feedback**: Student colors update in real-time
3. **Analytical Updates**: Matplotlib plots refresh every frame
4. **History Tracking**: Maintains 50-step history for trend analysis

## Technical Implementation Details

### Performance Optimizations

- **Limited History**: Only last 50 data points stored
- **Efficient Redraws**: Matplotlib plots update incrementally
- **Event-Driven**: Only processes necessary UI updates

### Memory Management

- Fixed-size data structures
- Automatic history pruning
- Efficient NumPy array operations

### Error Handling

- Input validation for all parameters
- Slider boundary checking
- Graceful shutdown

## Usage Examples

### Basic Operation

```python
# Create and run simulation
sim = EducationalSystemSimulation(num_students=25)
sim.run()
```

### Custom Parameter Setup

```python
sim = EducationalSystemSimulation()
sim.curriculum_content = 100
sim.teacher_skill = 0.9
sim.time_allotted = 60
sim.run()
```

## Educational Insights Demonstrated

### Systemic Effects

1. **Class Size Impact**: Larger classes increase effective demand through penalty function
2. **Teacher Quality**: Higher skill reduces effective demand linearly
3. **Curriculum Pressure**: More content in less time directly increases demand
4. **Time Constraints**: Limited time forces faster pacing

### Emergent Behavior

- **Threshold Effects**: Small parameter changes can cause large outcome shifts
- **Distribution Matters**: System performance depends on student ability distribution
- **Feedback Loops**: Failing students receive visual "labeling" (red coloring)

## Extension Possibilities

### Potential Enhancements

1. **Additional Parameters**
   - Student motivation factors
   - Classroom resources
   - Prior knowledge levels

2. **Advanced Models**
   - Time-dependent learning curves
   - Peer effects and social dynamics
   - Teacher adaptation mechanisms

3. **Visualization Improvements**
   - 3D parameter space exploration
   - Network graphs of student interactions
   - Longitudinal student tracking

### Research Applications

- Educational policy testing
- Classroom optimization studies
- Equity and inclusion analysis
- Resource allocation modeling

## Troubleshooting

### Common Issues

1. **Window Management**
   - Ensure both Pygame and Matplotlib windows are visible
   - Arrange windows side-by-side for optimal viewing
   - Reduce Matplotlib window if initially oversized.

2. **Performance**
   - Reduce update frequency if experiencing lag
   - Close other applications to free system resources

3. **Slider Sensitivity**
   - Click near slider handles for precise control
   - Small adjustments can have large effects due to system sensitivity


## License & Attribution

This simulation is designed for educational and research purposes. Please cite appropriately if used in academic work or publications.

## Buy me a Coffee

https://selar.com/showlove/judahx

---

*For questions or contributions, please contact me @ praisejames011@gmail.com*