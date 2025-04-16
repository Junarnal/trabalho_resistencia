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
  
  private:
    float lado;
    Vector2D centroide;
    bool subarea;
};

quadrado::quadrado(float lado, float centroide_x, float centroide_y, bool subarea = 1)
{
  rectangleShape quadrado(Vector2f(lado, lado));
  quadrado.setPosition(Vector2f(0.0f, 0.0f));
}

int main()
{
  sf::RenderWindow window(sf::VideoMode(640, 400), "Triangles and lines");
  window.setFramerateLimit(60);

  while(window.isOpen())
 
  {
    sf::Event event;
    while(window.pollEvent(event))
    {
      if(event.type == sf::Event::Closed)
        window.close();
    }

    window.clear(sf::Color(72, 77, 80, 0));

    window.display();
  }
  return 0;
}

