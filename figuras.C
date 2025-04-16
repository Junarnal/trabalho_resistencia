#include <iostream>
#include <list>
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>

using namespace sf;

class quadrado
{
  public:
    quadrado(float lado, float centroide_x, float centroide_y, bool subarea);
    RectangleShape quad;
    float lado;
    Vector2f centroide;
    bool subarea;
};

quadrado::quadrado(float lado, float centroide_x, float centroide_y, bool subarea = 1)
{
  RectangleShape quad = RectangleShape(Vector2f(lado, lado));
  quad.setPosition(Vector2f(0.0f, 0.0f));
}

int main()
{
  sf::RenderWindow window(sf::VideoMode(640, 400), "Triangles and lines");
  window.setFramerateLimit(60);

  float lado, x, y;

  std::cin >> lado >> x >> y;

  quadrado *quad = new quadrado(lado, x, y);

  while(window.isOpen())
 
  {
    sf::Event event;
    while(window.pollEvent(event))
    {
      if(event.type == sf::Event::Closed)
        window.close();
    }

    window.clear(sf::Color(72, 77, 80, 0));
    
    window.draw(quad->quad);

    window.display();
  }
  return 0;
}

