# Free Space Optical Propagation Turbulence Simulation
Simple FSO propagation library. Propagates a gaussian beam through the turbulent atmoshpere. Can be used to estimate link budget losses due to the atmospheric turbulence for a gaussian beam. 

**Usage**

1. Git clone or download the library
2. python -m pip install -r requirements.txt
3. python .\main.py

**Modify**

Parameters in the sim_config.json as needed. List of parameters accepted by *sim_config.json*.

| Parameter       | Description   | Units       | Notes |
| -------------   | ------------- |-------------|-------------|
| n_iterations    | Number of iterations  | - | Turbulent phase are generated randomly, increasing n_iterations gives a better approximation of turbulent phenomena | 
| sim_res         | Simulation resolution  | pixels | Too small values will introduce numerical artefacts |  
| sim_size        | Simulation size  | meters   | Too small values will introduce numerical artefacts |
| rx_alt          | Receiver altitude  | meters |      -       |-
| rx_diameter     | Receiver aperture diamter | meters        |       -      |
| wvl             | Wavelength  | meters      |       -      | 
| w0              | Beam waist  | meters      |       -      |
| power           | Beam power  | Watts       |       -      | 
| n_phase_screens | Number of turbulent phase screens  | -            | Typical number of phase screens used in AO simulation is 2-3 |
| r0              | Frieds parameter  | meters | Array, should be of size n_phase_screens | Typical values are 0.01 - 0.2 cm
| screen_alt      | Height of each turbulent layer  |  meters           | Array, should be of size n_phase_screens |
| l0              | Inner turbulence scale  |  meters          | Array, should be of size n_phase_screens. Typical value is 0.01 for all turbulent layers|
| L0              | Outter turbulence scale  | meters       | Array, should be of size n_phase_screens. Typical value is 50 for all turbulent layers            |

## Example Applications
### How to Estimate Losses caussed by Turbulence ?

**1.Simulate Turbulent Propagation**
```json
{
    "n_iterations":10,
    "sim_res": 4000,
    "sim_size": 40,
    "rx_alt": 500000,
    "rx_diameter": 0.09,
    "wvl": 1.55e-06,
    "w0": 0.021,
    "power": 0.1,
    "n_phase_screens": 2,
    "r0": [
        0.13,
        0.16
    ],
    "screen_alt": [
        1000.0,
        10000
    ],
    "l0": [
        0.01,
        0.01
    ],
    "L0": [
        50,
        50
    ]
}
```

| ![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/656ba242-76c5-4f4c-a297-9c0276180f7f)| 
|:--:| 
| *FSO propagation without turbulence* |

| ![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/bec6c7c1-562e-4602-a97a-64e4d3e57641)| 
|:--:| 
| *FSO turbulent propagation* |

**Output**

```
2024-04-18 00:58:17,343 INFO: Propagate beam without turbulence
2024-04-18 00:58:21,831 INFO: Total Losses no turbulence =  44.3290465655 dB
2024-04-18 00:58:21,832 INFO: Perform a simulation for 10 turbulent iterations
2024-04-18 01:01:27,793 INFO: Average Losses = 45.5994663001 dB
```

**2.Calculate Turbulence Losses**

```
Turbulence losses = Losses with turbulence - Losses without turbulence = 45.59 dB  -  44.32 dB = 1.27 dB
```

### **Other Example Simulations**

![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/71328fd6-879a-43f7-8ad5-fec775ab6a4f)
![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/bf415d49-0fd7-4813-9054-15187ec97dfb)
