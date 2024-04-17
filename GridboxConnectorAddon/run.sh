#!/usr/bin/with-contenv bashio

export MqttUser=$(bashio::config 'OverrideMqttUser')
export MqttPw=$(bashio::config 'OverrideMqttPw')
export MqttServer=$(bashio::config 'OverrideMqttServer')
export FiatChamp_MqttPort=$(bashio::config 'OverrideMqttPort')
  
test "$MqttUser" = "null" && export MqttUser=$(bashio::services "mqtt" "username")
test "$MqttPw" = "null" && export MqttPw=$(bashio::services "mqtt" "password")
test "$MqttServer" = "null" && export MqttServer=$(bashio::services "mqtt" "host")
test "$MqttPort" = "null" && export MqttPort=$(bashio::services "mqtt" "port")
export USERNAME=$(bashio::config 'username')
export PASSWORD=$(bashio::config 'password')
ls -lash /data
cat /data/options.json
cd /build/
ls -lash
pwd
python GridboxConnector
