class Api::AccountController < Api::ApiController

  skip_before_action :authenticate_user, only: %i[ login ]

  def unauthenticated
    @current_user = nil
  end

  def index
    success_response({'user': @current_user})
  end

  def login
    params.require([:username, :password])
    user = User.find_by(email: params[:username])
    unless user&.is_active and user.check_password(params[:password])
      # Maybe I can handle these errors using exceptions, so I do raise AuthorizationError and handle it somewhere else
      return validation_error("Unable to log in with provided credentials.", "authorization")
    end
    auth_token = AuthToken.create(user: user)
    # TODO return expiration date (when implemented)
    success_response({"user": user, "token": auth_token.token})
  end


end
