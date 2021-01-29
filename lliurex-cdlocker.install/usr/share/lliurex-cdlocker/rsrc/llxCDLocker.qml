import QtQuick 2.5
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2

ApplicationWindow {
	visible: true
	title: "LliureX CDLocker"
	property int margin: 1
	width: mainLayout.implicitWidth + 2 * margin
	height: mainLayout.implicitHeight + 2 * margin
	minimumWidth: mainLayout.Layout.minimumWidth + 2 * margin
	minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
	maximumWidth: mainLayout.Layout.maximumWidth + 2 * margin
	maximumHeight: mainLayout.Layout.maximumHeight + 2 * margin
	Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

   
    ColumnLayout {
    	id: mainLayout
        anchors.fill: parent
        anchors.margins: margin
       	Layout.minimumWidth:600	
        Layout.maximumWidth:600
        Layout.minimumHeight:350
        Layout.maximumHeight:350

        RowLayout {
        	id: bannerBox
        	Layout.alignment:Qt.AlignTop
        	Layout.minimumHeight:120
        	Layout.maximumHeight:120
        	Image{
        		id:banner
        		source: "/usr/share/lliurex-cdlocker/rsrc/lliurex-cdlocker.png"
       		}
       	}
        
        
        GroupBox{
        	id:gridBox
        	Layout.fillWidth: true
        	implicitWidth: 600
            implicitHeight:200
        	Layout.topMargin: 10
        	Layout.bottomMargin: 10
        	Layout.rightMargin:10
        	Layout.leftMargin:10
        	Layout.alignment:Qt.AlignTop

      		StackLayout {
                id: stackLayout
                currentIndex:0
                implicitWidth: 600
            	implicitHeight:200
				
	         	GridLayout {
	        		id: switchLayout
	                rows: 3
	                flow: GridLayout.TopToBottom
	                Layout.topMargin: 30
	                Layout.bottomMargin: 10
	                RowLayout {
	                	id: rowLayout
	                	Layout.topMargin: 10
	                	Layout.bottomMargin: 10
	                	Layout.fillWidth: true
	                	Layout.leftMargin:5
	                	
	                	Text {
	                		id:textMessage
	                		text: i18nd("lliurex-cdlocker","Lock clients CD trays")
			    			font.family: "Quattrocento Sans Bold"
			   				font.pointSize: 11
			    			color: "black"
			    			Layout.fillWidth: true
			    			Layout.preferredWidth: 75
						}   

		        		Switch {
		        			id:toggleswitch
		        			checked: con.loadState
		        			Layout.alignment:Qt.AlignVCenter
		        			Layout.fillWidth: true
  			
		        			indicator: Rectangle {
		        							implicitWidth: 40
							            	implicitHeight: 10
							            	x: toggleswitch.width - width - toggleswitch.rightPadding
							            	y: parent.height/2 - height/2 
							            	radius: 7
							            	color: toggleswitch.checked ? "deepskyBlue" : "lightGray"

							             	Rectangle {
						                		x: toggleswitch.checked ? parent.width - width : 0
						                   		width: 20
						                		height: 20
						                		y:parent.height/2-height/2
						                		radius: 10
						                		border.color: "grey"
						            		}
					        }
					      
		        			onToggled: {
		        				con.setState(toggleswitch.checked)
	    					}
							
						}
					}

					Rectangle {
						Layout.fillWidth: true
			    		Layout.preferredWidth: 85
        				Layout.leftMargin:5
			    		Layout.bottomMargin: 5
					    height: 1
					    border.color: "black"
					    border.width: 5
					    radius: 10
					}	
					
					RowLayout {
	                	id: rowHelp
	                	Layout.bottomMargin: 5
	                	Layout.leftMargin:5


						Text {
							id:helpText
							text: i18nd("lliurex-cdlocker","Allows you to lock / unlock the CD / DVD drive tray of the clients connected to the server. This prevents the tray from being manipulated by the client's users")
				    		font.family: "Quattrocento Sans"
				   			font.pointSize: 12
				    		color: "black"
				    		Layout.preferredWidth: 555
		     	    		wrapMode: Text.WordWrap
		     	    		horizontalAlignment: Text.AlignJustify

						}   
					}
				}
			}
       			
		}	
    }    
    
}