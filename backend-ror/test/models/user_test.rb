require "test_helper"

class UserTest < ActiveSupport::TestCase

  test 'should return correct role value' do
    user = User.create(password: "password", email: "scheduler@email.com", role: :scheduler)
    assert user.is_scheduler
    assert_not user.is_employee

    user = User.create(password: "password", email: "employee@email.com", role: :employee)
    assert user.is_employee
    assert_not user.is_scheduler

    # User creation shuold default role to employee
    user = User.create(password: "password", email: "employee_default@email.com")
    assert user.is_employee
    assert_not user.is_scheduler
  end

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
