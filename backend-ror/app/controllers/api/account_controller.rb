class Api::AccountController < Api::ApiController

  skip_before_action :authenticate_user, only: %i[ login register]

  def unauthenticated
    @current_user = nil
  end

  def index
    success_response({'user': @current_user})
  end

  def create_token_for_current_user
    # TODO return expiration date (when implemented)
    auth_token = AuthToken.create(user: @current_user)
    success_response({"user": @current_user, "token": auth_token.token})
  end

  def login
    params.require([:username, :password])
    user = User.find_by(email: params[:username])
    unless user&.is_active and user.check_password(params[:password])
      # Maybe I can handle these errors using exceptions, so I do raise AuthorizationError and handle it somewhere else
      return validation_error("Unable to log in with provided credentials.", "authorization")
    end
    @current_user = user
    create_token_for_current_user
  end

  def register
    @current_user = User.create(register_user_params)
    if @current_user
      create_token_for_current_user
    end
  end

  def register_user_params
    params.require([:email, :password])
    params.permit(:name, :email, :password, :role, :employee_id)
  end


end
