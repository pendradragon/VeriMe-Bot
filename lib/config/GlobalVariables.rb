module GlobalVariables
  @user_age = nil

  def self.user_age:
    @user_age
  end

  def self.user_age=(age):
    @user_age = age
  end

  $time_limit_days = 7 #default time. Can be set with the settime command

end