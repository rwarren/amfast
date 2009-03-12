package models
{
	[RemoteClass(alias="models.Email")]
	[Bindable]
	public class Email extends SAObject
	{
		public var id:Object;
		public var user_id:Object;
		public var label:String;
		public var email:String;
	}
}