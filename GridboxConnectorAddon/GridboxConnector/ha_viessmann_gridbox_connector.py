from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
from ha_viessmann_battery import HAViessmannBattery


class HAViessmannGridboxConnector:
    battery_sensor_dict: dict
    mqtt_settings: Settings.MQTT
    device_info: DeviceInfo
    production_sensor: Sensor
    grid_sensor: Sensor
    photovoltaic_sensor: Sensor
    consumption_household_sensor: Sensor
    total_consumption_household_sensor: Sensor
    direct_consumption_household_sensor: Sensor
    direct_consumtion_heatpump_sensor: Sensor
    direct_consumtion_rate_sensor: Sensor
    self_supply_sensor: Sensor
    self_consumtion_rate_sensor: Sensor
    self_sufficiency_rate_sensor: Sensor
    battery_sum: HAViessmannBattery

    def __init__(self, mqtt_settings):
        self.battery_sensor_dict = {}
        self.mqtt_settings = mqtt_settings
        self.device_info = DeviceInfo(
            name="Viessmann Gridbox", identifiers="viessmann_gridbox", manufacturer="Viessmann", model="Vitocharge 2.0")

        production_sensor_info = SensorInfo(name="Production", device_class="power",
                                            unique_id="gridbox_production", device=self.device_info, unit_of_measurement="W")
        production_settings = Settings(
            mqtt=mqtt_settings, entity=production_sensor_info)

        grid_sensor_info = SensorInfo(name="Grid", device_class="power",
                                      unique_id="gridbox_grid", device=self.device_info, unit_of_measurement="W")
        grid_settings = Settings(mqtt=mqtt_settings, entity=grid_sensor_info)

        photovoltaic_sensor_info = SensorInfo(name="Photovoltaic", device_class="power",
                                              unique_id="gridbox_photovoltaic", device=self.device_info, unit_of_measurement="W")
        photovoltaic_settings = Settings(
            mqtt=mqtt_settings, entity=photovoltaic_sensor_info)

        # consumption
        consumption_household_sensor_info = SensorInfo(
            name="Consumption", device_class="power", unique_id="gridbox_consumption_household", device=self.device_info, unit_of_measurement="W")
        consumption_household_settings = Settings(
            mqtt=mqtt_settings, entity=consumption_household_sensor_info)

        total_consumption_household_sensor_info = SensorInfo(
            name="Total Consumption", device_class="power", unique_id="total_consumption_household", device=self.device_info, unit_of_measurement="W")
        total_consumption_household_settings = Settings(
            mqtt=mqtt_settings, entity=total_consumption_household_sensor_info)

        # Direct Consumption
        direct_consumption_household_sensor_info = SensorInfo(
            name="DirectConsumptionHousehold", device_class="power", unique_id="gridbox_direct_consumption_household", device=self.device_info, unit_of_measurement="W")
        direct_consumption_household_settings = Settings(
            mqtt=mqtt_settings, entity=direct_consumption_household_sensor_info)

        direct_consumption_heatpump_sensor_info = SensorInfo(
            name="DirectConsumptionHeatPump", device_class="power", unique_id="gridbox_direct_consumption_heatpump", device=self.device_info, unit_of_measurement="W")
        direct_consumption_heatpump_settings = Settings(
            mqtt=mqtt_settings, entity=direct_consumption_heatpump_sensor_info)

        direct_consumption_rate_sensor_info = SensorInfo(
            name="DirectConsumptionRate", device_class="power_factor", unique_id="gridbox_direct_consumption_rate", device=self.device_info, unit_of_measurement="%")
        direct_consumption_rate_settings = Settings(
            mqtt=mqtt_settings, entity=direct_consumption_rate_sensor_info)

        # Self Consumption
        self_supply_sensor_info = SensorInfo(name="SelfSupply", device_class="power",
                                             unique_id="gridbox_self_supply", device=self.device_info, unit_of_measurement="W")
        self_supply_settings = Settings(
            mqtt=mqtt_settings, entity=self_supply_sensor_info)

        self_consumption_rate_sensor_info = SensorInfo(
            name="SelfConsumptionRate", device_class="power_factor", unique_id="gridbox_self_consumption_rate", device=self.device_info, unit_of_measurement="%")
        self_consumption_rate_settings = Settings(
            mqtt=mqtt_settings, entity=self_consumption_rate_sensor_info)

        self_sufficiency_rate_sensor_info = SensorInfo(
            name="SelfSufficiencyRate", device_class="power_factor", unique_id="gridbox_self_sufficiency_rate", device=self.device_info, unit_of_measurement="%")
        self_sufficiency_rate_settings = Settings(
            mqtt=mqtt_settings, entity=self_sufficiency_rate_sensor_info)

        # Instantiate the sensors

        self.production_sensor = Sensor(production_settings)
        self.grid_sensor = Sensor(grid_settings)
        self.photovoltaic_sensor = Sensor(photovoltaic_settings)

        # Battery sum
        self.battery_sum = HAViessmannBattery(
            mqtt_settings, self.device_info, "sum", "")

        # Consumption
        self.consumption_household_sensor = Sensor(
            consumption_household_settings)
        self.total_consumption_household_sensor = Sensor(
            total_consumption_household_settings)
        self.direct_consumption_household_sensor = Sensor(
            direct_consumption_household_settings)
        self.direct_consumtion_heatpump_sensor = Sensor(
            direct_consumption_heatpump_settings)
        self.direct_consumtion_rate_sensor = Sensor(
            direct_consumption_rate_settings)

        self.self_supply_sensor = Sensor(self_supply_settings)
        self.self_consumtion_rate_sensor = Sensor(
            self_consumption_rate_settings)
        self.self_sufficiency_rate_sensor = Sensor(
            self_sufficiency_rate_settings)

    def update_sensors(self, measurement: dict):
        if "production" in measurement:
            self.production_sensor.set_state(measurement.get("production", ""))
        if "grid" in measurement:
            self.grid_sensor.set_state(measurement.get("grid", ""))
        if "photovoltaic" in measurement:
            self.photovoltaic_sensor.set_state(measurement.get("photovoltaic", ""))
        if "consumption" in measurement:
            self.consumption_household_sensor.set_state(measurement.get("consumption", ""))
        if "totalConsumption" in measurement:
            self.total_consumption_household_sensor.set_state(measurement.get("totalConsumption", ""))
        if "directConsumptionHousehold" in measurement:
            self.direct_consumption_household_sensor.set_state(float(measurement.get("directConsumptionHousehold", "0")))
        if "directConsumptionHeatPump" in measurement:
            self.direct_consumtion_heatpump_sensor.set_state(float(measurement.get("directConsumptionHeatPump", "0")))
        if "directConsumptionRate" in measurement:
            self.direct_consumtion_rate_sensor.set_state(float(measurement.get("directConsumptionRate", "0"))*100)

        if "selfSupply" in measurement:
            self.self_supply_sensor.set_state(float(measurement.get("selfSupply", "")))
        if "selfConsumptionRate" in measurement:
            self.self_consumtion_rate_sensor.set_state(float(measurement.get("selfConsumptionRate", "0"))*100)
        if "selfSufficiencyRate" in measurement:
            self.self_sufficiency_rate_sensor.set_state(float(measurement.get("selfSufficiencyRate", "0"))*100)

        if "battery" in measurement:
            battery: dict = measurement.get("battery", {})
            state_of_charge = float(battery.get("stateOfCharge", "0"))*100
            capacity = float(battery.get("capacity", "0"))
            power = float(battery.get("power", "0"))
            remaining_charge = float(battery.get("remainingCharge", "0"))
            self.battery_sum.set_states(state_of_charge, capacity, power, remaining_charge)
        if "batteries" in measurement:
            batteries: list = measurement.get("batteries", [])
            for index, battery in enumerate(batteries):
                appliance_id = battery.get("applianceID", "")
                if appliance_id not in self.battery_sensor_dict:
                    self.battery_sensor_dict[appliance_id] = HAViessmannBattery(self.mqtt_settings, self.device_info, f"{index+1}", appliance_id)
                battery_sensor = self.battery_sensor_dict[appliance_id]
                state_of_charge = float(battery.get("stateOfCharge", "0"))*100
                capacity = float(battery.get("capacity", "0"))
                power = float(battery.get("power", "0"))
                remaining_charge = float(battery.get("remainingCharge", "0"))
                battery_sensor.set_states(state_of_charge, capacity, power, remaining_charge)