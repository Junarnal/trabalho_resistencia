#include <iostream>
#include <SFML/Graphics.hpp>

using namespace sf;
using namespace std;

int main()
{
  RenderWindow window(VideoMode(800, 600), "Calculadora de Momento de Inércia");
  window.setFramerateLimit(60);

  Vector2f center(400, 300);
  
  while(window.isOpen())
  {
    Event event;
    while(window.pollEvent(event))
    {
      if(event.type == Event::Closed)
      {
        window.close();
      }
      if(event.mouseButton.button == Mouse::Left)
      {
        Vector2f mouse_position = window.mapPixelToCoords(Mouse::getPosition(window));
        cout << mouse_position.x << ", " << mouse_position.y << endl;
      }
    }
    window.display();
  }

  return 0;
}
