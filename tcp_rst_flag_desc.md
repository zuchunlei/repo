#tcp rst 产生的原因
***
###概述
> 在TCP协议中，RST标识复位，用来异常的关闭链接。在TCP的设计中它是不可或缺的，发送RST包关闭链接时，不必等缓冲区的数据都发送出去。直接丢弃缓冲区中的数据，发送RST包。而接受段收到RST包后，也不必发送ACK包来确认。

##产生RST包的一些原因
####1. 请求的目标端口未打开，服务端发送RST包。
> ![连接未监听端口][image1] 

####2. 请求超时。

####3. Socket内核接受缓冲区Recv-Q中的数据未完全被应用程序读取，而关闭该Socket。
> ![socket recv-q存在数据][image2]
> *此时应用程序关闭socket链接对象。*
> ![关闭socket][image3]
> *产生RST段*

####4. 向已关闭的Socket中发送数据。（send与close调用）
> ![socket一端close][image4]
> *tcp一端调用close关闭。*
> ![socket另一端调用send向已关闭的socket发生数据][image5]
> *socket另一端调用send向已关闭的socket发送数据*
> ![socket一端调用close关闭][image6]
> *tcp一端调用close关闭，当前socket处于FIN_WAIT2定时器周期。*
> ![在已关闭socket的FIN_WAIT2定时器周期内调用close][image7]
> *tcp另一端在FIN_WAIT2定时器超时之前调用close方法，正常返回ACK确认包。*
> ![tcp一段close][image8]
> *tcp一端调用close关闭，当前socket处于FIN_WAIT2定时器周期。*
> ![FIN_WAIT2超时][image9]
> *FIN_WAIT2超时*
> ![tcp另一端在超时后调用close][image10]
> *tcp另一端在FIN_WAIT2超时后调用close*  
> **如果调用close()方法，关闭的Socket代表的链接依然处于FIN_WAIT2状态，则正常返回ACK确认包。如果状态FIN_WAIT2的超时，则close()调用后【向FIN_WAIT2超时状态的连接发送FIN】，依然会返回RST包。**

 [image1]:http://i5.tietuku.com/721e9627efd551fd.gif "连接未监听端口"
 [image2]:http://i12.tietuku.com/4ff30084a02ac36f.png "socket recv-q存在数据"
 [image3]:http://i12.tietuku.com/827ab12bc4cdc1e1.png "关闭socket"
 [image4]:http://i5.tietuku.com/4033b06f9c7e120a.png "socket一端close"
 [image5]:http://i5.tietuku.com/8061a0f861d7b55d.png "socket另一端调用send向已关闭的socket发生数据"
 [image6]:http://i5.tietuku.com/fc76d299e94ec663.png "socket一端调用close关闭"
 [image7]:http://i13.tietuku.com/764cfc91dbeb7968.png "在已关闭socket的FIN_WAIT2定时器周期内调用close"
 [image8]:http://i13.tietuku.com/b2e70daf171df684.png "tcp一端close"
 [image9]:http://i13.tietuku.com/502197421da27ee2.png "FIN_WAIT2超时"
 [image10]:http://i13.tietuku.com/9b6843d49b3b217b.png "tcp另一端在超时后调用close"
