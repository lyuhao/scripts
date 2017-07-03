import java.net._
import java.io._
import scala.io._
import java.util.concurrent.{Executors,ExecutorService}
import java.util.Date

class SocketHandler(socket:Socket) extends Runnable {

	def run() {
		val in = new BufferedReader(new InputStreamReader(socket.getInputStream))
		var ss = in.readLine()
     	var ssarray = ss.split(" ")
      	val appid = ssarray(1)
      	val numberexcutor = ssarray(2).toInt
      	val workerid = ssarray(0)
      	val out = new PrintStream(socket.getOutputStream())
      	println(workerid)
      	println(numberexcutor)
      	println(appid)
      	println("-------")
      	out.println('1')
      	socket.close()
	}
}


class ClientThread(port:Int,address:String,Message:String) extends Runnable {

	def run() {

		val s = new Socket(InetAddress.getByName(address),port)
		val out = new PrintStream(s.getOutputStream())
		println("sending message: " + Message)
		out.println(Message)
		out.flush()
		s.close()
	}
}


class ServerThread(port:Int, poolSize: Int) extends Runnable {
	val server = new ServerSocket(port)
	val pool: ExecutorService = Executors.newFixedThreadPool(poolSize)

	def run () {
		try {
			while (true) {
				val s = server.accept()
				pool.execute(new SocketHandler(s))
			}
		} finally {
			pool.shutdown()
		}
	}


}


object Server {
	def main(args: Array[String]): Unit = {
		(new ClientThread(9999,"localhost","app app1")).run
		(new ClientThread(9999,"localhost","worker worker1")).run
		//(new ServerThread(9990,2)).run
		return
	}
	

}
