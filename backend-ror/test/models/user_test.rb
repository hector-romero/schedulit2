require "test_helper"

class UserTest < ActiveSupport::TestCase
  test "should set hashed user password" do
    user = User.create(password: "password", email: "testemail@email.com")
    user = User.find(user.id)  # is this needed?
    assert_not_equal user.password, 'password'
    assert_nothing_raised do
      password = Password.decode(user.password)
      split = user.password.split('$', 4)
      assert_equal password.algorithm, split[0]
      assert_equal password.iterations, split[1].to_i
      assert_equal password.salt, split[2]
      assert_equal password.hash, split[3]
    end
  end

  test "should accept correct password" do
    user = User.create(password: "password", email: "testemail@email.com")

    assert user.check_password('password')
    assert_not user.check_password(user.password)
    assert_not user.check_password('wrong password')
  end
end
