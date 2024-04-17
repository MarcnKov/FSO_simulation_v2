# FSO_simulation_v2
Simple FSO propagation library. Propagates a gaussian beam through the turbulent atmoshpere. Can be used to estimate link budget losses due to the atmospheric turbulence for a gaussian beam. 

**Usage**

1. Git clone or download the library
2. python -m pip install -r requirements.txt 

**Modify**

Parameters in the sim_config.json as needed. List of parameters accepted by *sim_config.json*.

| Parameter       | Description   | Units       | Notes |
| -------------   | ------------- |-------------|-------------|
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

**1.Simulate Propagation with Turbulence**
```json
{
    "sim_res": 5000,
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
        10000.0
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
 ![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/bec6c7c1-562e-4602-a97a-64e4d3e57641)

**Output**
```
Total power = 0.1000000000 W
RX power =  0.0000014921 W
RX power =  -28.2619469559 dBm
Total Losses =  48.2619469559 dB
```

**2.Simulate Propagation without Turbulence**

```json
{
    "sim_res": 5000,
    "sim_size": 40,
    "rx_alt": 500000,
    "rx_diameter": 0.09,
    "wvl": 1.55e-06,
    "w0": 0.021,
    "power": 0.1,
    "n_phase_screens": 0,
    "r0": [],
    "screen_alt": [],
    "l0": [],
    "L0": []
}
```
![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/656ba242-76c5-4f4c-a297-9c0276180f7f)

**Output**

```
Total power = 0.0998677520 W
RX power =  0.0000033068 W
RX power =  -24.8059570454 dBm
Total Losses =  44.8059570454 dB
```

**3.Calculate Turbulence Losses**

```
Turbulence losses = Losses with turbulence - Losses without turbulence = 48.26 dB  - 44.80 dB = 3.46 dB
```

### **Other Example Simulations**

![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/71328fd6-879a-43f7-8ad5-fec775ab6a4f)
![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/bf415d49-0fd7-4813-9054-15187ec97dfb)
