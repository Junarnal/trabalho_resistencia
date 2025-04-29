#include <iostream>
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>

using namespace sf;

int main()
{
  RenderWindow window(VideoMode(100, 100), "Triangles and lines");
  window.setFramerateLimit(60);


  while(window.isOpen())
  {
    Event event;
    while(window.pollEvent(event))
    {
      if(event.type == Event::Closed)
        window.close();
    }

    // window.clear(Color(72, 77, 80, 0));
    window.clear();

    for(float i = 0.0; i < window.getSize().x; i = i + 2.0)
    {
      Vertex eixo_y[] = {Vertex(Vector2f(i, 0.0f)), Vertex(Vector2f(i, window.getSize().x))};
      window.draw(eixo_y, 2, Lines);
    }
    for(float i = 0.0; i < window.getSize().y; i = i + 2.0)
    {
      Vertex eixo_x[] = {Vertex(Vector2f(0.0f, i)), Vertex(Vector2f(window.getSize().y, i))};
      window.draw(eixo_x, 2, Lines);
    }

    window.display();
  }
  return 0;
}

