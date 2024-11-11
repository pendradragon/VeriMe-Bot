#Using the global variables
require_relative "../GlobalVariables"

module ConfigCommands
  def self.set_min_age(age):
    GlobalVariables.age = age
    "Age has been set to #{age}."

  end 

  def set_time_limit(days):
    GlobalVariables.time_limit_days = days
    "Time limit set to #{days} day(s)."
  end

end