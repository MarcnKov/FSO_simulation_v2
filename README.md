# FSO_simulation_v2
Simple FSO propagation library. Propgates a gaussian beam through the turbulent atmoshpere. Can be used to estimate link budget losses due to the atmospheric turbulence for laser propagation. 

**USAGE**

1. Git clone or download the library
2. python -m pip install -r requirements.txt 

**MODIFY**

Parameters in the sim_config.json as needed

List of parameters accepted by *sim_config.json*

| Parameter       | Description   | Units       | Constraints |
| -------------   | ------------- |-------------|-------------|
| sim_res         | Content Cell  |             |             |  
| sim_size        | Content Cell  |             |             |
| rx_alt          | Content Cell  |             |             |
| rx_diameter     | Content Cell  |             |             |
| wvl             | Content Cell  |             |             |
| w0              | Content Cell  |             |             |
| power           | Content Cell  |             |             |
| n_phase_screens | Content Cell  |             |             |
| max_turb_alt    | Content Cell  |             |             |
| min_turb_alt    | Content Cell  |             |             |
| r0              | Content Cell  |             |             |
| screen_alt      | Content Cell  |             |             |
| l0              | Content Cell  |             |             |
| L0              | Content Cell  |             |             |




**OUTPUT**

![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/71328fd6-879a-43f7-8ad5-fec775ab6a4f)
![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/bf415d49-0fd7-4813-9054-15187ec97dfb)
